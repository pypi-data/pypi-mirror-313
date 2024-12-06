import hashlib
import inspect
import json
import os
import warnings
from typing import Callable, Iterator, Optional, Union

import backoff
from pydantic import BaseModel, create_model

from base import ApiClient, Configuration, DefaultApi
from base.models.completion_api import CompletionAPI
from base.models.completion_request import CompletionRequest
from base.models.json_schema_api import JSONSchemaAPI
from base.models.json_schema_status import JSONSchemaStatus
from base.models.status import Status
from base.models.success import Success
from dottxt.config import Config


def lookup_max_poll_time():
    return int(os.getenv("DOTTXT_COMPILE_TIMEOUT", 1860))


def raise_timeout_error(msg: Optional[str] = ""):
    raise TimeoutError(msg)


class Dottxt:

    def __init__(self, config: Optional[Config] = None):
        """Construct a new instance of the dottxt client.

        This automatically loads the following arguments from the environment:
        - `api_key` from `DOTTXT_API_KEY`
        - `base_url` from `DOTTXT_BASE_URL`

        Parameters
        ----------
        config : Config
            Configuration to pass to the client
        """
        if config is None:
            config = Config()

        self.api_config = Configuration(
            host=config.base_url, access_token=config.api_key
        )
        self.api_client = ApiClient(self.api_config)
        self.default_api = DefaultApi(self.api_client)

    def create_schema(
        self,
        schema: Union[str, object, Callable],
        name: Optional[str] = None,
        wait: bool = True,
    ) -> JSONSchemaStatus:
        """Compile a JSON schema for use in structured generation.

        Parameters
        ----------
        schema : Union[str, object, Callable]
            The JSON Schema. Can be a JSON string, a Pydantic model, or a callable
            whose parameters and types define the schema.
        name : Optional[str]
            The name of the schema (the default is None, in which case a schema's source
            hash is used).
        wait : bool, default True
            If true, wait for schema compilation to complete before returning.
            If false, return schema status immediately.

        Returns
        -------
        JSONSchemaStatus
            Status object including schema name (`name`), identifier (`js_id`),
            status url (`status_url`), compilation status (`status`), and
            compilation detail (`detail`).

        References
        ----------
        .. [0] JSON Schema. https://json-schema.org/
        """
        schema_str = self._get_schema_str(schema)
        name = name or self._get_source_hash(schema_str)
        json_schema_api = JSONSchemaAPI(name=name, json_schema=schema_str)
        schema_status = self.default_api.structgen_api_public_create_json_schema(
            json_schema_api
        )
        if wait is False or schema_status.status != Status("in_progress"):
            return schema_status

        return self.poll_schema_status(schema_status.js_id)

    # Adapted from outlines:
    # https://github.com/dottxt-ai/outlines/blob/b55d31463cb6ed38fc0109e018f53ce0cdafbe19/outlines/fsm/json_schema.py#L527
    def _get_schema_from_signature(self, fn: Callable) -> str:
        signature = inspect.signature(fn)
        arguments = {}
        for name, arg in signature.parameters.items():
            if arg.annotation == inspect._empty:
                raise ValueError("Each argument must have a type annotation")
            else:
                arguments[name] = (arg.annotation, ...)

        try:
            fn_name = fn.__name__
        except Exception as e:
            fn_name = "Arguments"
            warnings.warn(
                "The function name could not be determined. Using"
                + "default name 'Arguments' instead. For debugging,"
                + f"here is exact error:\n{e}",
                category=UserWarning,
            )
        model = create_model(fn_name, **arguments)

        return model.model_json_schema()

    def _get_schema_str(self, schema: Union[str, object, Callable]) -> str:
        if isinstance(schema, type(BaseModel)):
            schema_str = json.dumps(schema.model_json_schema())
        elif callable(schema):
            schema_str = json.dumps(self._get_schema_from_signature(schema))
        elif isinstance(schema, str):
            schema_str = schema
        else:
            raise ValueError(
                "Invalid type for `schema`. The schema must be one of "
                + "a Pydantic object, a function or a string that contains the JSON "
                + "Schema specification"
            )
        return schema_str

    @backoff.on_predicate(
        backoff.expo,
        predicate=lambda x: x.status == Status("in_progress"),
        max_time=lookup_max_poll_time,
        base=1,
        on_giveup=lambda _: raise_timeout_error("Schema compilation timed out"),
    )
    def poll_schema_status(self, js_id: str) -> JSONSchemaStatus:
        """Poll for schema status until schema completes compiling."""
        return self.get_schema_status(js_id)

    def get_schema_status(self, js_id: str) -> JSONSchemaStatus:
        """Get JSON schema status by id.

        Get the compilation status of the schema corresponding to the given identifier.

        Parameters
        ----------
        js_id : str
            The JSON schema identifier.

        Returns
        -------
        JSONSchemaStatus
            Status object including schema name (`name`), identifier (`js_id`),
            status url (`status_url`), compilation status (`status`), and
            compilation detail (`detail`).
        """
        res: JSONSchemaStatus = (
            self.default_api.structgen_api_public_get_json_schema_status(js_id)
        )
        return res

    def list_schemas(self) -> Iterator[JSONSchemaStatus]:
        """List JSON schemas.

        Provides an iterator over JSON schemas.

        Yields
        ------
        JSONSchemaStatus
            Status object including schema name (`name`), identifier (`js_id`),
            status url (`status_url`), compilation status (`status`), and
            compilation detail (`detail`).
        """
        page_number = 1

        while True:
            res = self.default_api.structgen_api_public_list_json_schemas(
                page=page_number
            )
            if len(res.items) == 0:
                return
            yield from res.items
            page_number += 1

    def get_schema_status_by_name(self, name: str) -> Optional[JSONSchemaStatus]:
        """Lookup schema status by name.

        Parameters
        ----------
        name : str
            The name of the schema.

        Returns
        -------
        JSONSchemaStatus
            Status object including schema name (`name`), identifier (`js_id`),
            status url (`status_url`), compilation status (`status`), and
            compilation detail (`detail`).
        """
        res = self.default_api.structgen_api_public_list_json_schemas(name=name)
        if len(res.items) == 1:
            return res.items[0]
        return None

    def _get_normalized(self, source: str) -> str:
        """Remove unnecessary whitespace from the schema source."""
        return json.dumps(json.loads(source), separators=(",", ":"))

    def _get_source_hash(self, schema_str: str) -> str:
        """Function to get hash of a json schema."""
        hash_obj = hashlib.sha3_256()
        hash_input = self._get_normalized(schema_str)
        hash_obj.update(hash_input.encode())
        return hash_obj.hexdigest()

    def get_schema_status_by_source(
        self, schema: Union[str, object, Callable]
    ) -> Optional[JSONSchemaStatus]:
        """Lookup schema status by source.

        Parameters
        ----------
        schema : Union[str, object, Callable]
            The JSON Schema. Can be a JSON string, a Pydantic model, or a callable
            whose parameters and types define the schema.

        Returns
        -------
        JSONSchemaStatus
            Status object including schema name (`name`), identifier (`js_id`),
            status url (`status_url`), compilation status (`status`), and
            compilation detail (`detail`).
        """
        schema_str = self._get_schema_str(schema)
        source_hash = self._get_source_hash(schema_str)
        res = self.default_api.structgen_api_public_list_json_schemas(
            source_hash=source_hash
        )
        if len(res.items) == 1:
            return res.items[0]
        return None

    def get_schema(self, js_id: str) -> JSONSchemaAPI:
        """Get JSON schema corresponding to the given identifier.

        Parameters
        ----------
        js_id : str
            The JSON schema identifier.

        Returns
        -------
        JSONSchemaAPI
            JSON schema info including name (`name`) and schema string (`json_schema`).
        """
        return self.default_api.structgen_api_public_get_json_schema(js_id)

    def delete_schema(self, js_id: str) -> Success:
        """Delete the JSON schema corresponding to the given identifier.

        Parameters
        ----------
        js_id : str

        Returns
        -------
        Success
            Success object with boolean deletion status (`success`).
        """
        return self.default_api.structgen_api_public_delete_json_schema(js_id)

    def create_completion(
        self,
        prompt: str,
        js_id: str,
        max_tokens: Optional[int] = None,
        seed: Optional[int] = None,
    ) -> CompletionAPI:
        """Generate structured JSON data based on the specified JSON schema.

        Parameters
        ----------
        prompt : str
            Prompt to use for generation.
        js_id : str
            The JSON schema identifier.
        max_tokens : Optional[int]
            The maximum number of tokens to generate.
        seed : Optional[int]
            Sets the seed for reproducibility in LLM-generated outputs.

        Returns
        -------
        CompletionAPI
            Completion string (`data`) and API usage statistics (`usage`).
        """

        completion_request = CompletionRequest(
            prompt=prompt, max_tokens=max_tokens, seed=seed
        )
        return self.default_api.structgen_api_public_create_completion(
            js_id, completion_request
        )

    def json(
        self,
        prompt: str,
        schema: Union[str, object, Callable],
        max_tokens: Optional[int] = None,
        seed: Optional[int] = None,
    ) -> CompletionAPI:
        """Generate structured JSON data based on the provided schema.

        Create a new schema if there is no matching schema on the server. Wait for
        compilation to finish. Generate structured JSON data based on the provided
        schema. If schema already exists, the name field will be ignored.


        Parameters
        ----------
        prompt : str
            Prompt to use for generation.
        schema : Union[str, object, Callable]
            The JSON Schema. Can be a JSON string, a Pydantic model, or a callable
            whose parameters and types define the schema.
        name : Optional[str]
            Name of schema, used only if a new schema is created.
        max_tokens : Optional[int]
            The maximum number of tokens to generate.
        seed : Optional[int]
            Sets the seed for reproducibility in LLM-generated outputs.

        Returns
        -------
        CompletionAPI
            Completion string (`data`) and API usage statistics (`usage`).
        """
        schema_status = self.get_schema_status_by_source(schema)
        # Compile schema if lookup by source returns None
        if schema_status is None:
            schema_status = self.create_schema(schema=schema)
        # Create completion if schema is compiled
        if schema_status.status == Status("complete"):
            return self.create_completion(prompt, schema_status.js_id, max_tokens, seed)
        elif schema_status.status == Status("in_progress"):
            schema_status = self.poll_schema_status(schema_status.js_id)
            # Due to backoff decorator, mypy finds that schema_status
            # is not guaranteed to not be None, so we ignore type below
            return self.create_completion(
                prompt, schema_status.js_id, max_tokens, seed  # type: ignore
            )
        else:
            raise ValueError("Schema failed to compile.")

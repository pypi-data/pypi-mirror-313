import logging
import os
import typing
from json import JSONDecodeError
from typing import Optional, Type

import orjson
from loguru import logger
from postgrest.exceptions import APIError, generate_default_error_message
from pydantic import BaseModel
from supabase._async.client import AsyncClient
from supabase._async.client import create_client as async_create_client
from supabase.client import Client, ClientOptions, create_client
from tenacity import after_log, retry, stop_after_attempt, wait_exponential

from good_common.dependencies import AsyncBaseProvider, BaseProvider

from ._auth import GoogleAuthCallbackHandler

logging.getLogger("httpx").setLevel(logging.WARNING)

InsertableObject = dict | BaseModel
Insertable = InsertableObject | list[InsertableObject]


class SupabaseAsync:
    def __init__(
        self,
        client: AsyncClient,
        log_requests: bool = False,
    ):
        self._client = client

    @classmethod
    async def create(
        cls,
        url: str,
        key: str,
        schema: str = "public",
    ):
        client = await async_create_client(
            supabase_url=url,
            supabase_key=key,
            options=ClientOptions(
                schema=schema,
                postgrest_client_timeout=180,
            ),
        )
        return cls(client)

    @property
    def client(self) -> AsyncClient:
        return self._client

    def _preprocess_record(self, record: InsertableObject):
        if isinstance(record, BaseModel):
            return record.model_dump(mode="json", exclude_none=True)
        return record

    def _preprocess_data(self, data: Insertable):
        if not isinstance(data, list):
            data = [data]
        return [self._preprocess_record(record) for record in data]

    def _model_metadata(self, data: Insertable):
        if isinstance(data, list):
            _model = data[0]
        else:
            _model = data

        if isinstance(_model, BaseModel):
            model = _model.__class__
        elif isinstance(_model, dict):
            return {}

        fields = {}
        for name, field in model.model_fields.items():
            fields[name] = (field.json_schema_extra or {}).get("supabase", {})

        return {"model": model, "fields": fields}

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1.5, min=4, max=10),
        after=after_log(logger, logging.DEBUG),
        reraise=True,
    )
    async def upsert(
        self,
        table: str,
        data: Insertable,
        on_conflict: str | None = None,
        **kwargs,
    ):
        field_metadata = self._model_metadata(data)

        if on_conflict is None:
            _conflict_fields = []
            for field, metadata in field_metadata.get("fields").items():
                if metadata.get("primary_key") is True:
                    _conflict_fields.append(field)
                elif metadata.get("unique") is True:
                    _conflict_fields.append(field)
            if len(_conflict_fields) > 0:
                on_conflict = ",".join(_conflict_fields)
        response = None
        try:
            response = (
                await self.client.table(table)
                .upsert(
                    self._preprocess_data(data),
                    on_conflict=on_conflict,
                    **kwargs,
                )
                .execute()
            )
        except Exception as e:
            logger.error(e)
            if e.code == "21000":
                logger.info("inserting one by one")
                for row in data:
                    (
                        await self.client.table(table)
                        .upsert(
                            self._preprocess_data([row]),
                            on_conflict=on_conflict,
                            **kwargs,
                        )
                        .execute()
                    )

            # raise e
        if not response:
            return None
        if field_metadata.get("model"):
            output = [
                field_metadata.get("model").model_validate(record)
                for record in response.data
            ]
        else:
            output = response.data

        if isinstance(data, list):
            return output
        return output[0]

    async def fetch_all(
        self,
        table: str,
        columns: list[str] = ["*"],
        output_model: Type[BaseModel] = None,
    ):
        if output_model:
            columns = output_model.model_fields.keys()
        query = self.client.table(table).select(*columns)
        response = await query.execute()
        if output_model:
            return [output_model(**record) for record in response.data]
        return response.data

    async def fetch_filter(
        self,
        table: str,
        filter_func: typing.Callable,
        output_model: Type[BaseModel] | None = None,
    ):
        # columns = output_model.model_fields.keys()
        # logger.info(columns)
        response = await (filter_func(self.client.table(table).select("*"))).execute()
        if output_model:
            return [output_model(**record) for record in response.data]
        else:
            return response.data

    def google_auth(self, port: int = 9997):
        return GoogleAuthCallbackHandler(self.client, port)

    async def rpc(
        self,
        procedure: str,
        params: Optional[dict] = None,
        _cast_to: Optional[Type[BaseModel]] = None,
        _log: Optional[bool] = None,
        **_params,
    ):
        params = params or {}

        params.update(_params)

        _last_log = None
        _cast_to = _cast_to or params.pop("cast_to", None)
        _log = _log or params.pop("log", None)

        if _log is not None:
            _last_log = self._log_requests
            self._log_requests = _log

        query = self.client.postgrest.rpc(
            procedure,
            orjson.loads(
                orjson.dumps(params)
            ),  # ensures json properly serialized for requests
        )

        try:
            r = await query.execute()

        except Exception as e:
            raise APIError(str(e))

        try:
            return r
        except JSONDecodeError:
            raise APIError(generate_default_error_message(r))

        # if _log is not None:
        #     self._log_requests = _last_log

        # if data:
        #     if _cast_to and isinstance(data, dict):
        #         return _cast_to(**data)
        #     elif _cast_to and isinstance(data, list):
        #         return [_cast_to(**o) for o in data]
        #     return data
        return None


class Supabase:
    def __init__(
        self,
        client: Client,
        log_requests: bool = False,
    ):
        self._client = client
        self._log_requests = log_requests

    @property
    def client(self) -> Client:
        return self._client

    def log(self, msg: typing.Any):
        if self._log_requests:
            logger.info(msg)

    # @retry(
    #     stop=stop_after_attempt(2),
    #     wait=wait_exponential(multiplier=1, min=4, max=10)
    # )
    def rpc(
        self,
        procedure: str,
        params: Optional[dict] = None,
        _cast_to: Optional[Type[BaseModel]] = None,
        _log: Optional[bool] = None,
        **_params,
    ) -> typing.Any:
        params = params or {}

        params.update(_params)

        _last_log = None
        _cast_to = _cast_to or params.pop("cast_to", None)
        _log = _log or params.pop("log", None)

        if _log is not None:
            _last_log = self._log_requests
            self._log_requests = _log

        query = self.client.postgrest.rpc(
            procedure,
            orjson.loads(
                orjson.dumps(params)
            ),  # ensures json properly serialized for requests
        )

        try:
            r = query.execute()

        except Exception as e:
            raise APIError(str(e))

        try:
            return r
        except JSONDecodeError:
            raise APIError(generate_default_error_message(r))

        # if _log is not None:
        #     self._log_requests = _last_log

        # if data:
        #     if _cast_to and isinstance(data, dict):
        #         return _cast_to(**data)
        #     elif _cast_to and isinstance(data, list):
        #         return [_cast_to(**o) for o in data]
        #     return data
        # return None

    def _format_param_value(self, arg):
        # if isinstance(arg, dict):
        #     return orjson.dumps(arg).decode('utf-8')
        # if dataclasses.is_dataclass(arg):
        #     return orjson.dumps(dataclasses.asdict(arg)).decode('utf-8')
        return arg

    def _format_params(self, params: dict):
        return {
            k: self._format_param_value(v) for k, v in params.items() if v is not None
        }

    def google_auth(self, port: int = 9997):
        return GoogleAuthCallbackHandler(self.client, port)


class SupabaseProvider(BaseProvider[Supabase], Supabase):
    def _create_client(
        self,
        url: Optional[str] = None,
        key: Optional[str] = None,
        schema: Optional[str] = None,
        options: Optional[dict] = None,
    ):
        url = url or os.environ.get("SUPABASE_URL")
        key = key or os.environ.get("SUPABASE_KEY")

        if not url or not key:
            raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY")

        if not options:
            options = {}
        if schema:
            options["schema"] = schema

        supabase: Client = create_client(
            url, key, options=ClientOptions(postgrest_client_timeout=180, **options)
        )
        return supabase

    def __init__(
        self,
        url: Optional[str] = None,
        key: Optional[str] = None,
        schema: Optional[str] = None,
        **kwargs,
    ):
        kwargs["url"] = url
        kwargs["key"] = key
        kwargs["schema"] = schema
        super().__init__(**kwargs)

    def initializer(
        self,
        cls_args: typing.Tuple[typing.Any, ...],
        cls_kwargs: typing.Dict[str, typing.Any],
        fn_kwargs: typing.Dict[str, typing.Any],
    ):
        # print((cls_args, cls_kwargs, fn_kwargs))
        return cls_args, {
            "client": self._create_client(
                **{
                    **cls_kwargs,
                    **{k: v for k, v in fn_kwargs.items() if k in ["schema"]},
                }
            )
        }


class SupabaseAsyncProvider(AsyncBaseProvider[SupabaseAsync], SupabaseAsync):
    def __init__(
        self,
        url: Optional[str] = None,
        key: Optional[str] = None,
        schema: Optional[str] = None,
        **kwargs,
    ):
        kwargs["url"] = url or os.environ.get("SUPABASE_URL")
        kwargs["key"] = key or os.environ.get("SUPABASE_KEY")
        kwargs["schema"] = schema or os.environ.get("SUPABASE_SCHEMA", "public")
        super().__init__(**kwargs)

    @classmethod
    async def provide(cls, *args, **kwargs):
        return await SupabaseAsync.create(*args, **kwargs)

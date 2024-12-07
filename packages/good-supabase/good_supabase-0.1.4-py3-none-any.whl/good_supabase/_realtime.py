# import asyncio
# import os
# import typing

# from loguru import logger
# from pydantic import BaseModel, Field
# # from realtime.connection import Socket
# from realtime import AsyncRealtimeChannel, AsyncRealtimeClient
# # from realtime import AsyncRealtimeClient

# from good_common.dependencies import BaseProvider

# T = typing.TypeVar("T", bound=BaseModel | dict)


# class WebhookRecord(BaseModel, typing.Generic[T]):
#     id: int
#     created_at: str
#     domain: str
#     body: T | dict
#     event: str


# class ChannelMessage(BaseModel, typing.Generic[T]):
#     columns: typing.List[dict]
#     commit_timestamp: str
#     errors: typing.Optional[typing.Any]
#     record: WebhookRecord[T]
#     table_schema: str = Field(alias="schema")
#     table: str
#     type: str


# # class Channel:
# #     def __init__(self, socket: Socket, channel_name: str):
# #         self._socket = socket
# #         self._channel_name = channel_name
# #         self._queue = asyncio.Queue()
# #         self._listener = None
# #         self._stop = asyncio.Event()

# #     def channel_callback(self, message: dict):
# #         self._queue.put_nowait(message)

# #     async def __aenter__(self):
# #         await self._socket._connect()
# #         self._channel = self._socket.set_channel(self._channel_name)
# #         return self

# #     async def __aexit__(self, exc_type, exc_value, traceback):
# #         logger.info("Existing channel gracefully")
# #         self._stop.set()
# #         if self._listener:
# #             self._listener.cancel()

# #     async def listen(self):
# #         try:
# #             await asyncio.gather(self._socket._listen(), self._socket._keep_alive())
# #         except asyncio.CancelledError:
# #             pass
# #         except Exception as e:
# #             logger.info(("listen", e))
# #             self._stop.set()

# #     async def on(
# #         self,
# #         event: typing.Literal["insert", "update", "delete"],
# #         cast_as: typing.Type[T] | None = None,
# #     ) -> typing.AsyncGenerator[ChannelMessage[T], None]:
# #         try:
# #             await self._channel._join()  # type: ignore

# #             self._channel.on(event.upper(), self.channel_callback)  # type: ignore

# #             loop = asyncio.get_running_loop()

# #             self._listener = loop.create_task(self.listen())

# #             # loop.ad

# #             while not self._stop.is_set():
# #                 try:
# #                     message = await asyncio.wait_for(self._queue.get(), timeout=1)
# #                     # yield ChannelMessage[T](**message)
# #                     yield ChannelMessage[cast_as](**message) if cast_as else message
# #                 except asyncio.TimeoutError:
# #                     # continue  # Timeout reached, check the stop event again
# #                     continue
# #                 except asyncio.CancelledError:
# #                     self._stop.set()
# #                     break
# #                 except Exception as e:
# #                     logger.info(("on", e))
# #                     await asyncio.sleep(1)
# #                     return
# #         finally:
# #             self._listener.cancel()  # type: ignore
# #             # Ensure the listener task is cancelled when exiting
# #             try:
# #                 await self._listener  # type: ignore
# #                 # Wait for the listener task to be cancelled
# #             except asyncio.CancelledError:
# #                 pass

# #             return


# # class SupabaseRealtime:
# #     def __init__(
# #         self,
# #         supabase_id: str,
# #         supabase_key: str,
# #     ):
# #         self._supabase_id = supabase_id
# #         self._supabase_key = supabase_key

# #         self._socket = Socket(self._socket_url)

# #     @property
# #     def _socket_url(self) -> str:
# #         return (
# #             f"wss://{self._supabase_id}.supabase.co/realtime/v1"
# #             f"/websocket?apikey={self._supabase_key}&vsn=1.0.0"
# #         )

# #     def channel(self, channel_name: str):
# #         return Channel(self._socket, channel_name)

# #     async def __aenter__(self):
# #         return self

# #     async def __aexit__(self, exc_type, exc_value, traceback):
# #         logger.info(("aexit", exc_type, exc_value, traceback))
# #         await self._socket.close()


# # class SupabaseRealtimeProvider(BaseProvider[SupabaseRealtime], SupabaseRealtime):
# #     def __init__(
# #         self, supabase_id: str | None = None, supabase_key: str | None = None, **kwargs
# #     ):
# #         kwargs["supabase_id"] = supabase_id or os.environ["SUPABASE_ID"]
# #         kwargs["supabase_key"] = supabase_key or os.environ["SUPABASE_KEY"]
# #         super().__init__(**kwargs)

# #     def initializer(self, cls_args, cls_kwargs, fn_kwargs):
# #         cls_kwargs["supabase_id"] = fn_kwargs.get(
# #             "supabase_id", os.environ["SUPABASE_ID"]
# #         )
# #         cls_kwargs["supabase_key"] = fn_kwargs.get(
# #             "supabase_key", os.environ["SUPABASE_KEY"]
# #         )

# #         return cls_args, cls_kwargs

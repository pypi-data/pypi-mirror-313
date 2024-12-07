import asyncio
import logging
from datetime import datetime
from typing import Self, Optional, Literal

from chzzk import Chzzk
from chzzk.client import ChatClient
from chzzk.event import EventManager
from chzzk.exception import ChzzkError, ReconnectWebsocket
from chzzk.model import ChatContext, ChatMessage

_log = logging.getLogger(__name__)


class ChzzkChat(EventManager):
    def __init__(
            self,
            prefix: str = "!",
            chzzk: Optional[Chzzk] = None,
            loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        super().__init__(prefix=prefix, loop=loop)
        self._chzzk: Chzzk = chzzk or Chzzk()
        self._chat_client: Optional[ChatClient] = None
        self._context: ChatContext = ChatContext()
        self.is_closed = False
        self.is_reconnected = True
        
        # live state
        self._live_state: Optional[Literal["OPEN", "CLOSE"]] = None

    async def close(self) -> None:
        await super().close()

        async def _close():
            if self._chat_client and self._chat_client.is_connect:
                await self._chat_client.close()

        await asyncio.create_task(_close())

    async def run(self, channel_id: str, reconnect: bool = True):
        assert self._chat_client is None, "Already connected."

        if self.loop is None:
            self.loop = asyncio.get_event_loop()

        self._context.channel_id = channel_id
        self.is_reconnected = reconnect

        if self._context.chat_channel_id is None and self._context.channel_id is not None:
            live = await self._chzzk.live.status(self._context.channel_id)
            if live is None:
                raise ChzzkError(msg="Connection to the server failed with CHZZK.")
            self._context.chat_channel_id = live.chat_channel_id

        if self._context.chat_channel_id and self._context.access_token is None:
            if self._chzzk.has_credentials():
                user = await self._chzzk.me()
                self._context.uid = user.user_id_hash

            token = await self._chzzk._game_chat.access_token(self._context.chat_channel_id)
            self._context.access_token = token.access_token
            self._context.extra_token = token.extra_token

        await self.polling()

    async def _check_live(self):
        _log.info(msg=f"check live status...")
        live_status = await self._chzzk.live.status(channel_id=self._context.channel_id)
        if live_status is None:
            return

        if self._live_state != live_status.status:
            self._live_state = live_status.status
            if self._live_state == "OPEN":
                self.dispatch("broadcast_open")
            elif self._live_state == "CLOSE":
                self.dispatch("broadcast_close")

        if live_status.chat_channel_id == self._context.chat_channel_id:
            return

        _log.info("A chat_channel_id has been updated. Reconnect websocket.")
        await self._chat_client.close()

        self._context.chat_channel_id = live_status.chat_channel_id
        raise ReconnectWebsocket()

    async def polling(self) -> None:
        while not self.is_closed:
            try:
                self._chat_client = ChatClient(context=self._context, parsers=self._parser.parsers)
                await self._chat_client.connect()

                last_check_time = datetime.now()

                while True:
                    await self._chat_client.poll_event()
                    relative_time = datetime.now() - last_check_time
                    if relative_time.total_seconds() >= 59:
                        last_check_time = datetime.now()
                        await self._check_live()

            except ReconnectWebsocket:
                self.dispatch("disconnect")
                if self.is_reconnected is False:
                    break
                continue

    async def send_chat(self, message: str) -> None:
        assert self._chat_client is not None, "ChatClient was not created properly."
        assert self._context.chat_channel_id is not None, "chatChannelId is None."
        await self._chat_client.send_chat(message=message, chat_channel_id=self._context.chat_channel_id)

    async def request_recent_chat(self, count: int = 50) -> None:
        assert self._chat_client is not None, "ChatClient was not created properly."
        assert self._context.chat_channel_id is not None, "chatChannelId is None."
        await self._chat_client.request_recent_chat(count=count, chat_channel_id=self._context.chat_channel_id)

    async def pin_message(self, message: ChatMessage) -> None:
        assert self._context.chat_channel_id is not None, "chatChannelId is None."
        assert message.created_time is not None, \
            "createdTime field of Message is empty. Please report this issue to developer."
        assert message.extras is not None, \
            "extras field of Message is empty. Please report this issue to developer."
        await asyncio.sleep(1)
        await self._chzzk._game_chat.set_notice_message(
            channel_id=self._context.chat_channel_id,
            extras=message.extras.model_dump_json(by_alias=True),
            message=message.content,
            message_time=int(message.created_time.timestamp()*1000),
            message_user_id_hash=message.user_id,
            streaming_channel_id=message.extras.streaming_channel_id
        )

    async def unpin_message(self) -> None:
        assert self._context.chat_channel_id is not None, "chatChannelId is None."
        await self._chzzk._game_chat.delete_notice_message(channel_id=self._context.chat_channel_id)

    async def blind_message(self, message: ChatMessage) -> None:
        assert self._context.chat_channel_id is not None, "chatChannelId is None."
        assert message.created_time is not None, \
            "createdTime field of Message is empty. Please report this issue to developer."
        assert message.extras is not None, \
            "extras field of Message is empty. Please report this issue to developer."
        await self._chzzk._game_chat.blind_message(
            channel_id=self._context.chat_channel_id,
            message=message.content,
            message_time=int(message.created_time.timestamp() * 1000),
            message_user_id_hash=message.user_id,
            streaming_channel_id=message.extras.streaming_channel_id
        )

    @property
    def is_broadcast_on(self):
        return self._live_state == "OPEN"

import asyncio
import json
import logging
import time
from typing import Optional, Any, Callable

import websockets
from websockets import ConnectionClosedError, ConnectionClosedOK
from websockets.asyncio.client import ClientConnection

from chzzk.exception import ChzzkError, ReconnectWebsocket, ConnectionClosed, WebSocketClosure
from chzzk.model import ChatContext, ChatCmd, DefaultPacket, get_enum, ChatType


_log = logging.getLogger()


class ChatClient:
    def __init__(self, context: ChatContext, parsers: dict[ChatCmd, Callable[..., Any]]):
        self._ws: Optional[ClientConnection] = None
        self.session_id = None
        self._context = context
        self._connect = False
        self._defaults = DefaultPacket(cid=self._context.chat_channel_id, svcid="game", ver="2")

        self._event_hook: dict[ChatCmd, Optional[Callable[..., Any]]] = {
            key: parsers[key] if parsers.get(key) else None for key in list(ChatCmd)
        }

    def set_hook(self, cmd: ChatCmd, coro: Callable[..., Any]):
        self._event_hook[cmd] = coro

    def remove_hook(self, cmd: ChatCmd):
        self._event_hook[cmd] = None

    @staticmethod
    def _can_handle_close(code: int) -> bool:
        """Check if a reconnection is possible."""
        # Define reconnection logic based on the close code
        return code in {1000, 1001}  # Example: Normal closure codes

    @property
    def is_connect(self) -> bool:
        if self._connect is None or self._ws is None:
            return False
        return True

    async def close(self) -> None:
        assert self.is_connect is True, "Not connected."
        self.session_id = None
        if self._ws:
            await self._ws.close()

    async def connect(self) -> None:
        assert self._context.chat_channel_id, "chatChannelId is None."
        server_id: int = sum(map(lambda x: ord(x), list(self._context.chat_channel_id))) % 9 + 1
        try:
            self._ws = await websockets.connect(f"wss://kr-ss{server_id}.chat.naver.com/chat")
            self._connect = True
            await self.send_open()
        except Exception as e:
            raise ChzzkError(msg=f"Chat 서버와의 연결에 실패했습니다. error: {e}")

    async def poll_event(self):
        try:
            msg = await asyncio.wait_for(self._ws.recv(decode=True), timeout=59)
            await self.received_message(json.loads(msg))
        except asyncio.TimeoutError:
            # await self.send_ping()
            pass
        except (WebSocketClosure, ConnectionClosedError, ConnectionClosedOK) as e:
            if self._can_handle_close(e.code):
                raise ReconnectWebsocket()
            else:
                raise ConnectionClosed(self._ws, e.code)

    async def received_message(self, data: dict[str, Any]) -> None:
        cmd: int = data["cmd"]
        body = data.get("bdy")

        cmd_type = get_enum(ChatCmd, cmd)

        match cmd_type:
            case ChatCmd.CONNECTED:
                if body is not None:
                    self.session_id = body["sid"]
            case ChatCmd.PING:
                await self.send_pong()
                return
            case ChatCmd.PERMISSION:
                if data.get("retCode") != 0:
                    _log.error("PERMISSON MISS ERROR:"
                               "Credentials are required, or you lack sufficient account permissions.")
                    func = self._event_hook.get(cmd_type)
                    if func is not None:
                        func(data)
                return

        func = self._event_hook.get(cmd_type)
        if func is not None:
            func(body)

    async def send(self, data: str):
        assert self._ws is not None, "Not connected."
        await self._ws.send(data)

    async def send_json(self, data: dict[str, Any]) -> None:
        assert self._ws is not None, "Not connected."
        await self._ws.send(json.dumps(data, ensure_ascii=False))

    async def send_pong(self):
        assert self._ws is not None, "Not connected."
        await self._ws.send(json.dumps({
            "cmd": ChatCmd.PONG,
            "ver": 2
        }))

    async def send_ping(self):
        assert self._ws is not None, "Not connected."
        await self._ws.send(json.dumps({
            "cmd": ChatCmd.PING,
            "ver": 2
        }))

    async def send_open(self):
        data = {
            "cmd": ChatCmd.CONNECT,
            "tid": 1,
            "bdy": {
                "accTkn": self._context.access_token,
                "auth": "SEND" if self._context.uid else "READ",
                "devType": 2001,
                "uid": self._context.uid
            }
        }
        data.update(self._defaults.model_dump(by_alias=True))
        await self.send_json(data)

    async def send_chat(self, message: str, chat_channel_id: str):
        extra = {
            "chatType": "STREAMING",
            "emojis": {},
            "osType": "PC",
            "streamingChannelId": chat_channel_id,
        }

        if self._context.extra_token:
            extra["extraToken"] = self._context.extra_token

        data = {
            "bdy": {
                "extras": json.dumps(extra),
                "msg": message,
                "msgTime": int(time.time() * 1000),
                "msgTypeCode": ChatType.TEXT,
            },
            "retry": False,
            "cmd": ChatCmd.SEND_CHAT,
            "sid": self.session_id,
            "cid": chat_channel_id,
            "tid": 3,
        }
        data.update(self._defaults.model_dump(by_alias=True))
        await self.send_json(data)

    async def request_recent_chat(self, count: int, chat_channel_id: str):
        data = {
            "bdy": {"recentMessageCount": count},
            "cmd": ChatCmd.REQUEST_RECENT_CHAT,
            "sid": self.session_id,
            "cid": chat_channel_id,
            "tid": 2,
        }
        data.update(self._defaults.model_dump(by_alias=True))
        await self.send_json(data)

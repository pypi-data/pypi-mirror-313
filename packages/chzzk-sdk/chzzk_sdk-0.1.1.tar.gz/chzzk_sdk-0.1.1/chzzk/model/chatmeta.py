from __future__ import annotations

from enum import Enum, IntEnum
from dataclasses import dataclass
from typing import Optional, TypeVar, Any


E = TypeVar("E", bound="Enum")


@dataclass
class ChatContext:
    chat_channel_id: Optional[str] = None
    channel_id: Optional[str] = None
    polling: Optional[int] = None
    access_token: Optional[str] = None
    extra_token: Optional[str] = None
    uid: Optional[str] = None


class ChatType(IntEnum):
    TEXT = 1
    IMAGE = 2
    STICKER = 3
    VIDEO = 4
    RICH = 5
    DONATION = 10
    SUBSCRIPTION = 11
    SYSTEM_MESSAGE = 30
    OPEN = 121


class ChatCmd(IntEnum):
    PING = 0
    PONG = 10000
    CONNECT = 100
    CONNECTED = 10100
    REQUEST_RECENT_CHAT = 5101
    RECENT_CHAT = 15101
    EVENT = 93006
    CHAT = 93101
    DONATION = 93102
    KICK = 94005
    BLOCK = 94006
    BLIND = 94008
    NOTICE = 94010
    PENALTY = 94015
    SEND_CHAT = 3101
    PERMISSION = 13101


def get_enum(cls: type[E], val: Any) -> E:
    enum_val = [i for i in cls if i.value == val]
    if len(enum_val) == 0:
        return val

    return enum_val[0]


class UserRole(Enum):
    common_user = "common_user"
    streamer = "streamer"
    chat_manager = "streaming_chat_manager"
    channel_manager = "streaming_channel_manager"
    manager = "manager"

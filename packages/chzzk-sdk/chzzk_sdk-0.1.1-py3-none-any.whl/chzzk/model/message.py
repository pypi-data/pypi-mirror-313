from __future__ import annotations

from datetime import datetime
from typing import Optional, Any, Literal, Generic, TypeVar, Annotated

from pydantic import Field, AliasChoices, Json, AfterValidator

from chzzk.model import DefaultModel, Profile, ChatType, ChatDonation, VideoDonation, MissionDonation, DonationBase
from chzzk.utils import to_kst, as_kst

T = TypeVar("T", bound="ExtraBase | DonationBase")


class ExtraBase(DefaultModel):
    pass


class Extra(ExtraBase):
    chat_type: str
    emojis: Optional[Any] = None
    os_type: Literal["PC", "AOS", "IOS"]
    streaming_channel_id: str
    extraToken: Optional[str] = None


class NoticeExtra(Extra):
    register_profile: Profile


class ChatDonationExtra(ChatDonation):
    pass


class VideoDonationExtra(VideoDonation):
    pass


class MissionDonationExtra(MissionDonation):
    pass


class SubscriptionExtra(ExtraBase):
    month: int
    tier_name: str
    nickname: Optional[str] = None
    tier_no: Optional[int] = None


class SystemExtraParameter(DefaultModel):
    register_nickname: str
    target_nickname: str
    register_chat_profile: Json[Profile] = Field(alias="registerChatProfileJson")
    target_profile: Json[Profile] = Field(alias="targetChatProfileJson")


class SystemExtra(ExtraBase):
    description: str
    style_type: int
    visible_roles: list[str]
    params: Optional[SystemExtraParameter] = None


class Message(DefaultModel, Generic[T]):
    service_id: str = Field(validation_alias=AliasChoices("serviceId", "svcid"))
    channel_id: str = Field(validation_alias=AliasChoices("channelId", "cid"))
    user_id: str = Field(validation_alias=AliasChoices("userId", "uid"))

    profile: Optional[Json[Profile]]
    content: str = Field(validation_alias=AliasChoices("msg", "content"))
    type: ChatType = Field(validation_alias=AliasChoices("msgTypeCode", "messageTypeCode"))
    extras: Optional[Json[T]]

    created_time: Optional[Annotated[datetime, AfterValidator(as_kst)]] = Field(
        validation_alias=AliasChoices("ctime", "createTime")
    )
    updated_time: Optional[Annotated[datetime, AfterValidator(as_kst)]] = Field(
        default=None, validation_alias=AliasChoices("utime", "updateTime")
    )
    message_time: Optional[Annotated[datetime, AfterValidator(as_kst)]] = Field(
        validation_alias=AliasChoices("msgTime", "messageTime")
    )


class MessageDetail(Message[T], Generic[T]):
    member_count: int = Field(validation_alias=AliasChoices("mbrCnt", "memberCount"))
    message_status: Optional[str] = Field(
        validation_alias=AliasChoices("msgStatusType", "messageStatusType")
    )

    # message_tid: ???
    # session: bool

    @property
    def is_blind(self) -> bool:
        return self.message_status == "BLIND"


class RecentChat(DefaultModel):
    message_list: list[ChatMessage]
    user_count: Optional[int]
    notice: Optional[NoticeMessage] = None


class PermissionMiss(DefaultModel):
    ret_code: Optional[int]
    ret_msg: Optional[str]


class ChatMessage(MessageDetail[Extra]):
    pass


class NoticeMessage(Message[NoticeExtra]):
    pass


class DonationMessage(MessageDetail[ChatDonationExtra | VideoDonationExtra | MissionDonationExtra]):
    pass


class SubscriptionMessage(MessageDetail[SubscriptionExtra]):
    pass


class SystemMessage(MessageDetail[SystemExtra]):
    pass

from typing import Any, Optional

from pydantic import PrivateAttr, Field, Json

from chzzk.model import DefaultModel, UserRole


class Badge(DefaultModel):
    name: Optional[str] = None
    image_url: Optional[str] = None


class ColorCode(DefaultModel):
    color_code: Optional[str] = None


class Subscription(DefaultModel):
    accumulative_month: Optional[int] = None
    badge: Optional[Badge] = None
    tier: Optional[int] = None


class StreamingProperty(DefaultModel):
    activated_achievement_badge_dds: list[Any] = Field(default_factory=list)
    nickname_color: Optional[ColorCode] = None
    real_time_donation_ranking: Optional[Badge] = None
    subscription: Optional[Subscription] = None


class ActivityBadge(DefaultModel):
    badge_no: int
    badge_id: str
    image_url: Optional[str] = None
    description: Optional[str] = None
    activated: bool


class Profile(DefaultModel):
    user_id_hash: str
    user_role: Optional[UserRole] = Field(alias="userRoleCode", default=None)
    nickname: str
    profile_image_url: Optional[str]
    _badge: Optional[dict[str, str]] = PrivateAttr(default=None)
    _title: Optional[dict[str, str]] = PrivateAttr(default=None)
    streaming_property: Optional[StreamingProperty] = None
    activity_badges: list[ActivityBadge] = Field(default_factory=list)
    verified_mark: bool = False

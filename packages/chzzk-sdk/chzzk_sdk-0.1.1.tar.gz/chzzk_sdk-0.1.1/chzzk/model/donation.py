from __future__ import annotations

from datetime import datetime
from typing import Optional, Literal, Annotated

from pydantic import Field, AliasChoices, AfterValidator

from chzzk.model import DefaultModel
from chzzk.utils import to_kst


class DonationRank(DefaultModel):
    user_id_hash: str
    nickname: str = Field(validation_alias=AliasChoices("nickname", "nickName"))
    verified_mark: bool
    donation_amount: int
    ranking: int


class DonationBase(DefaultModel):
    is_anonymous: bool = True
    pay_type: str
    pay_amount: int = 0
    donation_type: str
    weekly_rank_list: list[DonationRank] = Field(default_factory=list)
    donation_user_weekly_rank: Optional[DonationRank] = None


class ChatDonation(DonationBase):
    donation_type: Literal["CHAT"]


class VideoDonation(DonationBase):
    donation_type: Literal["VIDEO"]


class MissionDonation(DonationBase):
    donation_type: Literal["MISSION", "MISSION_PARTICIPATION"]
    duration_time: int = 0
    mission_donation_id: Optional[str] = None
    mission_donation_type: Optional[str] = None  # ALONE ?
    related_mission_donation_id: Optional[str] = None

    total_pay_amount: Optional[int] = 0
    mission_created_time: Optional[Annotated[datetime, AfterValidator(to_kst)]]
    mission_start_time: Optional[Annotated[datetime, AfterValidator(to_kst)]] = None
    mission_end_time: Optional[Annotated[datetime, AfterValidator(to_kst)]] = None
    mission_text: str

    status: str | Literal["PENDING", "REJECTED", "APPROVED", "COMPLETED"]
    success: bool = False

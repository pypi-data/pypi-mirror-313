from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Any, Annotated

from pydantic import AfterValidator, BeforeValidator

from chzzk.model import DefaultModel
from chzzk.utils import to_kst, convert


class Following(DefaultModel):
    following: bool
    notification: bool
    follow_date: Optional[Annotated[datetime, AfterValidator(to_kst)]] = None


class PersonalData(DefaultModel):
    private_user_block: bool
    following: Optional[Following] = None


class User(DefaultModel):
    has_profile: bool
    user_id_hash: Optional[str]
    nickname: Optional[str]
    profile_image_url: Optional[str]
    penalties: Optional[List[Any]]
    official_noti_agree: bool
    official_noti_agree_updated_date: Optional[Annotated[datetime, BeforeValidator(convert), AfterValidator(to_kst)]] = None
    verified_mark: bool
    logged_in: bool

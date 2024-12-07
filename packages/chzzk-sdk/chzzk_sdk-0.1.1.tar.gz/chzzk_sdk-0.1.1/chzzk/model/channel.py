from __future__ import annotations

from typing import List, Optional

from chzzk.model import DefaultModel
from chzzk.model.user import PersonalData


class PartialChannel(DefaultModel):
    channel_id: Optional[str] = None
    channel_name: str
    channel_image_url: Optional[str] = None
    verified_mark: bool
    activated_channel_badge_ids: Optional[List[str]] = None
    personal_data: Optional[PersonalData] = None


class Channel(PartialChannel):
    channel_type: Optional[str] = None  # STREAMING
    channel_description: str
    follower_count: int
    open_live: bool

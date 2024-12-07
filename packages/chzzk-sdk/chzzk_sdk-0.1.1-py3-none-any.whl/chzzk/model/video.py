from __future__ import annotations

from datetime import datetime
from typing import Annotated, Optional

from pydantic import AfterValidator

from chzzk.model import DefaultModel
from chzzk.model.channel import PartialChannel
from chzzk.utils import to_kst, as_kst


class VideoMetadata(DefaultModel):
    video_no: int
    video_id: str
    video_title: str
    video_type: str
    publish_date: Annotated[datetime, AfterValidator(to_kst)]
    thumbnail_image_url: str
    duration: int
    read_count: int
    channel_id: Optional[str] = None
    publish_date_at: Annotated[datetime, AfterValidator(as_kst)]
    category_type: Optional[str] = None
    video_category: str
    video_category_value: str


class PartialVideo(VideoMetadata):
    trailer_url: Optional[str] = None
    exposure: bool
    adult: bool
    clip_active: bool
    live_pv: int
    channel: PartialChannel
    blind_type: Optional[str] = None  # New
    watch_timeline: Optional[str] = None  # New


class Video(PartialVideo):
    paid_promotion: bool
    in_key: str
    live_open_date: Annotated[datetime, AfterValidator(to_kst)]
    vod_status: str

    prev_video: Optional[PartialVideo] = None
    next_video: Optional[PartialVideo] = None

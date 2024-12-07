from __future__ import annotations

from datetime import datetime
from typing import Literal, List, Optional, Any, Annotated, Union

from pydantic import Json, AfterValidator, Field

from chzzk.model import DefaultModel
from chzzk.model.channel import PartialChannel
from chzzk.utils import to_kst


class LivePollingStatus(DefaultModel):
    status: str
    is_publishing: bool
    playable_status: str
    traffic_throttling: int
    call_period_millisecond: int = Field(alias="callPeriodMilliSecond")


class LivePlaybackMetaCDNInfo(DefaultModel):
    cdn_type: str
    zero_rating: bool


class LivePlaybackMeta(DefaultModel):
    video_id: str
    stream_seq: int
    live_id: str
    paid_live: bool
    cdn_info: LivePlaybackMetaCDNInfo
    p2p: bool


class LivePlaybackServiceMeta(DefaultModel):
    content_type: str


class LivePlaybackLive(DefaultModel):
    start: Annotated[datetime, AfterValidator(to_kst)]
    open: Annotated[datetime, AfterValidator(to_kst)]
    time_machine: bool
    status: str


class LivePlaybackAPI(DefaultModel):
    name: str
    path: str


class LivePlaybackVideoTrack(DefaultModel):
    encoding_track_id: str
    video_profile: str
    audio_profile: str
    video_codec: str
    video_bit_rate: int
    audio_bit_rate: int
    video_frame_rate: float
    video_width: int
    video_height: int
    audio_sampling_rate: int
    audio_channel: int
    avoid_reencoding: bool
    video_dynamic_range: str


class LivePlaybackAudioTrack(DefaultModel):
    encoding_track_id: str
    path: str
    audio_codec: str
    audio_bit_rate: int
    audio_only: bool
    audio_sampling_rate: int
    audio_channel: int
    avoid_reencoding: bool


class LivePlaybackMedia(DefaultModel):
    media_id: str
    protocol: str
    path: str
    latency: Optional[str] = None
    encoding_track: List[Union[LivePlaybackVideoTrack, LivePlaybackAudioTrack]]


class LivePlaybackThumbnail(DefaultModel):
    snapshot_thumbnail_template: str
    time_machine_thumbnail_template: Optional[str] = None
    types: List[str]


class LivePlayback(DefaultModel):
    meta: LivePlaybackMeta
    service_meta: LivePlaybackServiceMeta
    live: LivePlaybackLive
    api: List[LivePlaybackAPI]
    media: List[LivePlaybackMedia]
    thumbnail: LivePlaybackThumbnail
    multiview: List[Any]


class Live(DefaultModel):
    live_title: str
    live_image_url: str
    default_thumbnail_image_url: Optional[str] = None
    concurrent_user_count: int
    accumulate_count: int
    open_date: Annotated[datetime, AfterValidator(to_kst)]
    live_id: int
    adult: bool
    tags: List[str]
    chat_channel_id: str
    category_type: Optional[str] = None
    live_category: Optional[str] = None
    live_category_value: str
    drops_campaign_no: Optional[str] = None
    channel_id: Optional[str] = None
    live_playback: Json[LivePlayback] = Field(alias="livePlaybackJson")


class LiveDetail(Live):
    status: str
    close_date: Optional[Annotated[datetime, AfterValidator(to_kst)]] = None
    chat_active: bool
    chat_available_group: str
    paid_promotion: bool
    chat_available_condition: str
    min_follower_minute: int
    channel: PartialChannel
    live_polling_status: Json[LivePollingStatus] = Field(alias="livePollingStatusJson")


class LiveStatus(DefaultModel):
    live_title: str
    status: Literal["OPEN", "CLOSE"]
    concurrent_user_count: int
    accumulate_count: int
    paid_promotion: bool
    adult: bool
    kr_only_viewing: bool
    clip_active: bool
    chat_channel_id: str
    tags: List[str]
    category_type: str
    live_category: str
    live_category_value: str
    live_polling_status: Json[LivePollingStatus] = Field(alias="livePollingStatusJson")
    fault_status: Optional[str]
    chat_active: bool
    chat_available_group: Any
    chat_available_condition: Any
    min_follower_minute: int
    allow_subscriber_in_follower_mode: bool
    chat_donation_ranking_exposure: bool
    drops_campaign_no: Any
    live_token_List: List[Any]

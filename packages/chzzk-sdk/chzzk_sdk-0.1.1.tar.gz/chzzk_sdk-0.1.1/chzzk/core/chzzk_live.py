from chzzk.client import ChzzkClient
from chzzk.model import LiveStatus, LiveDetail


class ChzzkLive:
    def __init__(self, client: ChzzkClient):
        self._chzzk_client = client

    async def status(self, channel_id: str) -> LiveStatus:
        response = await self._chzzk_client.get(f"polling/v2/channels/{channel_id}/live-status")
        return LiveStatus(**response)

    async def detail(self, channel_id: str) -> LiveDetail:
        response = await self._chzzk_client.get(f"service/v2/channels/{channel_id}/live-detail")
        return LiveDetail(**response)

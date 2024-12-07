from chzzk.client import ChzzkClient
from chzzk.model import Channel


class ChzzkChannel:
    def __init__(self, client: ChzzkClient):
        self._chzzk_client = client

    async def channel(self, channel_id: str) -> Channel:
        response = await self._chzzk_client.get(f"service/v1/channels/{channel_id}")
        return Channel(**response)

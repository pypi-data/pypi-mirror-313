from chzzk.client import ChzzkClient, GameClient
from chzzk.model import Video


class ChzzkVideo:
    def __init__(self, client: ChzzkClient):
        self._chzzk_client = client

    async def video(self, video_no: str) -> Video:
        response = await self._chzzk_client.get(f"polling/v2/videos/{video_no}")
        return Video(**response)

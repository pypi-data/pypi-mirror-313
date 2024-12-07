from chzzk.client import ChzzkClient
from chzzk.model import SearchCursor, ChannelSearchRecord, LiveSearchRecord, VideoSearchRecord


class ChzzkSerach:
    def __init__(self, client: ChzzkClient):
        self._chzzk_client = client

    async def channels(self, keyword: str, size: int = 10, offset: int = 0) -> SearchCursor[ChannelSearchRecord]:
        response = await self._chzzk_client.get(
            f"service/v1/search/channels",
            params={"keyword": keyword, "size": size, "offset": offset}
        )
        return SearchCursor[ChannelSearchRecord](**response)

    async def lives(self, keyword: str, size: int = 10, offset: int = 0) -> SearchCursor[LiveSearchRecord]:
        response = await self._chzzk_client.get(
            f"service/v1/search/lives",
            params={"keyword": keyword, "size": size, "offset": offset}
        )
        return SearchCursor[LiveSearchRecord](**response)

    async def videos(self, keyword: str, size: int = 10, offset: int = 0) -> SearchCursor[VideoSearchRecord]:
        response = await self._chzzk_client.get(
            f"service/v1/search/videos",
            params={"keyword": keyword, "size": size, "offset": offset}
        )
        return SearchCursor[VideoSearchRecord](**response)
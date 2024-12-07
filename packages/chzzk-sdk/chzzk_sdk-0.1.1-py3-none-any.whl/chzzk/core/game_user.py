from chzzk.client import GameClient
from chzzk.exception import ChzzkError
from chzzk.model import User


class GameUser:
    def __init__(self, client: GameClient):
        self._game_client = client

    async def me(self) -> User:
        if not self._game_client.has_credentials():
            raise ChzzkError(msg=f"Missing credentials. Please provide valid credentials to proceed.")
        response = await self._game_client.get("v1/user/getUserStatus")
        return User(**response)

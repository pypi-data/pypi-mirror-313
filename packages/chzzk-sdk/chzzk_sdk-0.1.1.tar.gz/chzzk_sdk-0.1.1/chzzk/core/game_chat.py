from chzzk.client import GameClient
from chzzk.exception import ChzzkError
from chzzk.model import Token


class GameChat:
    def __init__(self, client: GameClient):
        self._game_client = client

    async def access_token(self, chat_channel_id: str) -> Token:
        response = await self._game_client.get(
            f"v1/chats/access-token",
            params={"channelId": chat_channel_id, "chatType": "STREAMING"}
        )
        return Token(**response)

    async def set_notice_message(
            self,
            channel_id: str,
            extras: str,
            message: str,
            message_time: int,
            message_user_id_hash: str,
            streaming_channel_id: str,
    ) -> None:
        if not self._game_client.has_credentials():
            raise ChzzkError(msg="Missing credentials. Please provide valid credentials to proceed.")

        await self._game_client.post(
            f"v1/chats/notices",
            json={
                "channelId": channel_id,
                "chatType": "STREAMING",
                "message": message,
                "messageTime": message_time,
                "messageUserIdHash": message_user_id_hash,
                "streamingChannelId": streaming_channel_id,
                "extras": extras
            }
        )

    async def delete_notice_message(self, channel_id: str) -> None:
        if not self._game_client.has_credentials():
            raise ChzzkError(msg="Missing credentials. Please provide valid credentials to proceed.")

        await self._game_client.delete(
            f"v1/chats/notices",
            json={
                "channelId": channel_id,
                "chatType": "STREAMING"
            }
        )

    async def blind_message(
            self,
            channel_id: str,
            message: str,
            message_time: int,
            message_user_id_hash: str,
            streaming_channel_id: str
    ) -> None:
        if not self._game_client.has_credentials():
            raise ChzzkError(msg="Missing credentials. Please provide valid credentials to proceed.")

        await self._game_client.post(
            f"v1/chats/blind-message",
            json={
                "channelId": channel_id,
                "chatType": "STREAMING",
                "message": message,
                "messageTime": message_time,
                "messageUserIdHash": message_user_id_hash,
                "streamingChannelId": streaming_channel_id
            }
        )

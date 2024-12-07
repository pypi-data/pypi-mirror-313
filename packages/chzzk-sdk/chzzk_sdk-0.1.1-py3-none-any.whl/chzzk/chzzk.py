from __future__ import annotations
from typing import Optional

from chzzk.client import Credential, ChzzkClient, GameClient
from chzzk.core import ChzzkLive, ChzzkSerach, ChzzkChannel, ChzzkVideo, GameUser, GameChat


class Chzzk(ChzzkChannel, ChzzkVideo, GameUser):
    def __init__(self, credential: Optional[Credential] = None):
        self._credential = credential
        self._chzzk_client = ChzzkClient(credential)
        self._game_client = GameClient(credential)
        ChzzkChannel.__init__(self, self._chzzk_client)
        ChzzkVideo.__init__(self, self._chzzk_client)
        GameUser.__init__(self, self._game_client)

        self._live = ChzzkLive(self._chzzk_client)
        self._serach = ChzzkSerach(self._chzzk_client)
        self._game_chat = GameChat(self._game_client)

    @classmethod
    def from_data(cls, auth: str, session: str) -> Chzzk:
        return cls(Credential(auth=auth, session=session))

    def has_credentials(self):
        if self._credential is not None and self._credential.auth and self._credential.session:
            return True
        return False

    @property
    def search(self) -> ChzzkSerach:
        return self._serach

    @property
    def live(self) -> ChzzkLive:
        return self._live

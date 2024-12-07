from typing import ClassVar, Optional, Literal, Mapping, Any, Final
from urllib.parse import urljoin

import httpx

from chzzk.client.credential import Credential
from chzzk.exception import ChzzkHTTPError, ChzzkError

_http_method = Literal["GET", "POST", "DELETE"]
_user_agent: Final[str] = (
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"
)
_headers: Final[dict] = {
    "User-Agent": _user_agent
}


class Client:
    BASE_URL: ClassVar[str]

    def __init__(self, credential: Optional[Credential] = None):
        assert self.BASE_URL.endswith("/")

        self._client = httpx.AsyncClient(headers=_headers)

        self._credential = credential
        if self._credential is not None:
            self._client.cookies.update(self._credential.as_cookie())

    def has_credentials(self):
        if self._credential is not None and self._credential.auth and self._credential.session:
            return True
        return False

    async def request(
            self,
            method: _http_method,
            url: str,
            *,
            params: Optional[Mapping[str, Any]] = None,
            data: Optional[Mapping[str, Any]] = None,
            **kwargs
    ) -> Any:
        response = await self._client.request(
            method=method,
            url=urljoin(self.BASE_URL, url),
            params=params,
            data=data,
            **kwargs
        )
        assert not url.startswith("/"), "URL should not start with a slash(/)."
        if response.is_error:
            raise ChzzkHTTPError(code=response.status_code, msg=response.text)

        payload = response.json()
        if payload["code"] != 200:
            raise ChzzkHTTPError(code=payload["code"], msg=payload["message"])

        return payload["content"]

    async def get(
            self,
            url: str,
            *,
            params: Optional[Mapping[str, Any]] = None,
            **kwargs
    ) -> Any:
        return await self.request(method="GET", url=url, params=params, **kwargs)

    async def post(
            self,
            url: str,
            *,
            params: Optional[Mapping[str, Any]] = None,
            data: Optional[Mapping[str, Any]] = None,
            **kwargs
    ) -> Any:
        return await self.request(method="POST", url=url, params=params, data=data, **kwargs)

    async def delete(
            self,
            url: str,
            *,
            params: Optional[Mapping[str, Any]] = None,
            data: Optional[Mapping[str, Any]] = None,
            **kwargs
    ) -> Any:
        return await self.request(method="DELETE", url=url, params=params, data=data, **kwargs)


class ChzzkClient(Client):
    BASE_URL = "https://api.chzzk.naver.com/"

    def __init__(self, credential: Optional[Credential] = None):
        super().__init__(credential)


class GameClient(Client):
    BASE_URL = "https://comm-api.game.naver.com/nng_main/"

    def __init__(self, credential: Optional[Credential] = None):
        super().__init__(credential)

from dataclasses import dataclass

import httpx


@dataclass
class Credential:
    """
    auth: NID_AUT
    session: NID_SES
    """
    auth: str
    session: str

    def as_cookie(self) -> httpx.Cookies:
        cookies = httpx.Cookies()
        cookies.set(name="NID_AUT", value=self.auth, domain=".naver.com", path="/")
        cookies.set(name="NID_SES", value=self.session, domain=".naver.com", path="/")
        return cookies

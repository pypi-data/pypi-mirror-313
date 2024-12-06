import os
from typing import Literal
from requests import Session

DEFAULT_BASE_URL = "https://sourcestack-api.com"


class Client:
    api_key: str
    base_url: str

    def __init__(
        self,
        api_key: str | None = os.getenv("SOURCESTACK_API_KEY"),
        base_url: str | None = os.getenv("SOURCESTACK_BASE_URL"),
    ):
        if not api_key:
            raise ValueError("api_key is required")
        self.api_key = api_key
        self.base_url = base_url or DEFAULT_BASE_URL

    @property
    def session(self) -> Session:
        session = Session()
        session.headers.update({"X-API-KEY": self.api_key})
        return session

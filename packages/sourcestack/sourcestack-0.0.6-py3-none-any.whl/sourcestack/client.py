import os

from requests import Session

from sourcestack.jobs import Jobs

DEFAULT_BASE_URL = "https://sourcestack-api.com"


class Client:
    api_key: str
    base_url: str

    def __init__(
        self,
        api_key: str | None = os.getenv("SOURCESTACK_API_KEY"),
        base_url: str | None = os.getenv("SOURCESTACK_BASE_URL"),
    ):
        """
        Initializes the client with the api key and base url.

        Args:
            api_key (str): The api key to authenticate with the SourceStack API (required).
            base_url (str): The base url of the SourceStack API (optional).
        """
        if not api_key:
            raise ValueError("api_key is required")
        self.api_key = api_key
        self.base_url = base_url or DEFAULT_BASE_URL

    @property
    def session(self) -> Session:
        """
        Builds a session with the api key.

        Returns:
            request.Session: A session configured with the api key.
        """
        session = Session()
        session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "X-API-KEY": self.api_key,
            }
        )
        return session

    @property
    def jobs(self) -> Jobs:
        """
        Returns a jobs resource.

        Returns:
            Jobs: A jobs resource used to retrieve jobs from the SourceStack API.
        """
        return Jobs(session=self.session, base_url=self.base_url)

from requests import Session


class Resource:
    session: Session
    base_url: str

    def __init__(
        self,
        session: Session,
        base_url: str,
    ):
        """
        Initializes with a client and a base_url.

        Args:
            session (requests.Session): A session to use.
            base_url (str): The base url of the SourceStack API.

        """
        self.session = session
        self.base_url = base_url

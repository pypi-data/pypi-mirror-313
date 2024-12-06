from typing import Any, Dict, List
from urllib.parse import urljoin

from requests import Session

from sourcestack.resource import Resource

type Job = Dict[str, Any]


# https://sourcestack.co/docs/example-queries/#jobs
class Jobs(Resource):
    def all(self) -> List[Job]:
        """
        Fetches all jobs from the SourceStack API.

        Returns:
            List[Dict[str, Any]]: A list of jobs.
        """
        return self._get()

    def by_name(self, name: str, exact: bool = False) -> List[Job]:
        """
        Fetches jobs by name from the SourceStack API.

        Args:
            name (str): The name of the job.
            exact (bool): Whether to match the name exactly.

        Returns:
            List[Dict[str, Any]]: A list of jobs.
        """
        return self._get(name=name, exact="true" if exact else "false")

    def by_parent(self, parent: str) -> List[Job]:
        """
        Fetches jobs by parent from the SourceStack API.

        Args:
            parent (str): The parent of the job.

        Returns:
            List[Dict[str, Any]]: A list of jobs.
        """
        return self._get(parent=parent)

    def by_url(self, url: str) -> List[Job]:
        """
        Fetches jobs by url from the SourceStack API.

        Args:
            url (str): The url of the job.

        Returns:
            List[Dict[str, Any]]: A list of jobs.
        """
        return self._get(url=url)

    def by_uses_product(self, uses_product: str, exact: bool = True) -> List[Job]:
        """
        Fetches jobs by product from the SourceStack API.

        Args:
            product (str): The product of the job.
            exact (bool): Whether to match the product exactly.

        Returns:
            List[Dict[str, Any]]: A list of jobs.
        """
        return self._get(uses_product=uses_product, exact="true" if exact else "false")

    def by_uses_category(self, uses_category: str, exact: bool = True) -> List[Job]:
        """
        Fetches jobs by category from the SourceStack API.

        Args:
            category (str): The category of the job.
            exact (bool): Whether to match the category exactly.

        Returns:
            List[Dict[str, Any]]: A list of jobs.
        """
        return self._get(
            uses_category=uses_category, exact="true" if exact else "false"
        )

    def _get(self, **kwargs) -> List[Job]:
        url = urljoin(self.base_url, "jobs")
        response = self.session.get(url, params=kwargs)
        response.raise_for_status()
        return response.json()

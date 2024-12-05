from .base import KrameriusBaseClient
from ..schemas import SearchParams


class StatisticsClient:
    def __init__(self, client: KrameriusBaseClient):
        self._client = client

    def search(self, search_params: SearchParams):
        return self._client.admin_request(
            "GET", "statistics/search", params=search_params.build()
        )

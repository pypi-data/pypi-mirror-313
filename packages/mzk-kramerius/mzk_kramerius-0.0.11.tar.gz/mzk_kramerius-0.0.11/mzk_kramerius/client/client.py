from .base import KrameriusBaseClient
from .items import ItemsClient
from .processing import ProcessingClient
from .sdnnt import SdnntClient
from .search import SearchClient
from .statistics import StatisticsClient


class KrameriusClient:
    def __init__(
        self,
        host: str,
        keycloak_host: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        username: str | None = None,
        password: str | None = None,
        timeout: int | None = None,
        max_retries: int | None = None,
    ):
        self._base = KrameriusBaseClient(
            host,
            keycloak_host,
            client_id,
            client_secret,
            username,
            password,
            timeout,
            max_retries,
        )

        self.Items = ItemsClient(self._base)
        self.Processing = ProcessingClient(self._base)
        self.Sdnnt = SdnntClient(self._base)
        self.Search = SearchClient(self._base)
        self.Statistics = StatisticsClient(self._base)

from .base import KrameriusBaseClient
from lxml import etree


class ItemsClient:
    def __init__(self, client: KrameriusBaseClient):
        self._client = client

    def get_mods(self, pid) -> etree._ElementTree | None:
        return etree.fromstring(
            self._client.client_request_response(
                "GET",
                f"items/{pid}/metadata/mods",
            ).content
        )

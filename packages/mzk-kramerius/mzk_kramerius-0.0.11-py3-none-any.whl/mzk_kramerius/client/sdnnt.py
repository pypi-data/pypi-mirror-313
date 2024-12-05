from .base import KrameriusBaseClient
from ..schemas import (
    SdnntResponse,
    SdnntGranularityResponse,
    SdnntGranularityRecord,
)
from datetime import datetime, timezone


PAGE_SIZE = 100


class SdnntClient:
    def __init__(self, client: KrameriusBaseClient):
        self._client = client

    def get_sdnnt_timestamp(self, tzinfo=timezone.utc):
        return datetime.strptime(
            self._client.admin_request("GET", "sdnnt/sync/timestamp")
            .get("docs")[0]
            .get("fetched"),
            "%Y-%m-%dT%H:%M:%S.%fZ",
        ).replace(tzinfo=tzinfo)

    def get_sdnnt_changes(self, page: int, rows: int) -> SdnntResponse:
        return SdnntResponse.model_validate(
            self._client.admin_request(
                "GET", f"sdnnt/sync?rows={rows}&page={page}"
            )
        )

    def iterate_sdnnt_changes(self):
        page = 0
        num_found = self.get_sdnnt_changes(page, 0).numFound

        while page * PAGE_SIZE < num_found:
            response = self.get_sdnnt_changes(page, PAGE_SIZE)
            for doc in response.docs:
                yield doc
            page += 1

    def get_sdnnt_granularity(self, id: str) -> SdnntGranularityResponse:
        return [
            SdnntGranularityRecord.model_validate(record)
            for record in self._client.admin_request(
                "GET", f"sdnnt/sync/granularity/{id}"
            ).get(id)
        ]

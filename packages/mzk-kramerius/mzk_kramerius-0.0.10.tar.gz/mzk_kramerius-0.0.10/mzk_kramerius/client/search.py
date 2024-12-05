from .base import KrameriusBaseClient
from ..datatypes import Field, Params, Pid
from ..schemas import SearchParams, SearchQuery, base_, KrameriusDocument
from typing import List

PAGINATE_PAGE_SIZE = 100


class SearchClient:
    def __init__(self, client: KrameriusBaseClient):
        self._client = client

    def _search(self, params: Params):
        return self._client.client_request("GET", "search", params)

    def get_document(self, pid: Pid):
        params = SearchParams(query=base_(Field.Pid, pid).build(), rows=1)
        response = self._search(params.build())
        return (
            KrameriusDocument(response["response"]["docs"][0])
            if response["response"]["numFound"] > 0
            else None
        )

    def num_found(self, query: SearchQuery | str):
        return self._search(
            SearchParams(
                query=(
                    query.build() if isinstance(query, SearchParams) else query
                ),
                rows=0,
            ).build()
        )["response"]["numFound"]

    def search(self, query: SearchQuery | str, fl: List[Field] | None = None):
        query = query.build() if isinstance(query, SearchQuery) else query

        params = SearchParams(query=query, rows=PAGINATE_PAGE_SIZE, fl=fl)

        numFound = self.num_found(query)

        if numFound <= PAGINATE_PAGE_SIZE:
            for document in self._search(params.build())["response"]["docs"]:
                yield KrameriusDocument(document)
            return

        params = params.with_pagination()

        while True:
            response = self._search(params.build())

            for document in response["response"]["docs"]:
                yield KrameriusDocument(document)

            numFound = response["response"]["numFound"]
            nextCursorMark = response["nextCursorMark"]

            if nextCursorMark == params.cursorMark:
                break
            params.cursorMark = nextCursorMark

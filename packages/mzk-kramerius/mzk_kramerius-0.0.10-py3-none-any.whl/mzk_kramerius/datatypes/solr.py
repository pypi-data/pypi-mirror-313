from enum import Enum
from typing import List, Tuple, Union


SolrValue = Union[str, int, float, List, Tuple, Enum]

Wildcard = "*"

StartCursorMark = "*"


class SolrConjuction(Enum):
    And = " AND "
    Or = " OR "

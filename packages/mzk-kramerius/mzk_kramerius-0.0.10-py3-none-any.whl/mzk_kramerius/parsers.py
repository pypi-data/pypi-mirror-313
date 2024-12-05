import re
from typing import Optional


VOLUME_YEAR = r"^\s*(\d{4})\s*$"
VOLUME_RANGE = r"^\s*(\d{4})-(\d{4})?\s*$"
VOLUME_MULTIYEAR = r"^\s*(?:(\d{4}),\s*)+(\d{4})\s*$"


def range_start_year(year: Optional[str]) -> Optional[int]:
    if year is None:
        return None
    match = re.match(VOLUME_YEAR, year)
    if match:
        return int(match.group(1))
    match = re.match(VOLUME_RANGE, year)
    if match:
        return int(match.group(1))
    match = re.match(VOLUME_MULTIYEAR, year)
    if match:
        return min(int(group) for group in match.groups())


def range_end_year(year: Optional[str]) -> Optional[int]:
    if year is None:
        return None
    match = re.match(VOLUME_YEAR, year)
    if match:
        return int(match.group(1))
    match = re.match(VOLUME_RANGE, year)
    if match:
        return int(match.group(2))
    match = re.match(VOLUME_MULTIYEAR, year)
    if match:
        return max(int(group) for group in match.groups())

from enum import Enum


class TreePredicate(Enum):
    HasPage = "hasPage"
    HasPart = "hasPart"
    HasVolume = "hasVolume"
    HasItem = "hasItem"
    HasUnit = "hasUnit"
    HasIntCompPart = "hasIntCompPart"
    IsOnPage = "isOnPage"

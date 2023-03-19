from pydantic import BaseModel
from beanie import Document, PydanticObjectId
from typing import Optional
from models.watchList import WatchList


class Profile_in(BaseModel):
    name: str
    index: Optional[int]
    watchLists: list[PydanticObjectId] = []

    icon: Optional[str]
    theme: Optional[str]

    def toJSON(self):
        watchListsJSON = ""
        for watchList in self.watchLists:
            watchListsJSON += watchList.__str__() + ", "
        watchListsJSON = watchListsJSON[:-2]

        string = (
            "{"
            + f'"name": "{self.name}", "index": {self.index}, "watchLists": ['
            + '"'
            + watchListsJSON
            + '"'
            + "], "
            + f'"icon": "{self.icon}", "theme": "{self.theme}"'
            + "}"
        )
        return string


class Profile(Document, Profile_in):
    id: PydanticObjectId = PydanticObjectId()

    def toJSON(self):
        watchListsJSON = ""
        for watchList in self.watchLists:
            watchListsJSON += watchList.__str__() + ", "
        watchListsJSON = watchListsJSON[:-2]

        string = (
            "{"
            + f'"id": "{self.id}", "name": "{self.name}", "index": {self.index}, "watchLists": ['
            + '"'
            + watchListsJSON
            + '"'
            + "], "
            + f'"icon": "{self.icon}", "theme": "{self.theme}"'
            + "}"
        )
        return string

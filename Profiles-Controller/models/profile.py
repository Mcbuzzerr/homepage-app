from pydantic import BaseModel
from beanie import Document, PydanticObjectId
from typing import Optional
from models.watchList import WatchList


class Profile_in(BaseModel):
    name: str
    index: Optional[int]
    watchLists: list[WatchList] = []

    icon: Optional[str]
    theme: Optional[str]

    def toJSON(self):
        string = (
            "{"
            + f'"name": "{self.name}", "index": {self.index}, "watchLists": ['
            + ", ".join(self.watchLists)
            + "], "
            + f'"icon": "{self.icon}", "theme": "{self.theme}"'
            + "}"
        )
        return string


class Profile(Document, Profile_in):
    id: PydanticObjectId = PydanticObjectId()

    def toJSON(self):
        string = (
            "{"
            + f'"id": "{self.id}", "name": "{self.name}", "index": {self.index}, "watchLists": ['
            + ", ".join(self.watchLists)
            + "], "
            + f'"icon": "{self.icon}", "theme": "{self.theme}"'
            + "}"
        )
        return string

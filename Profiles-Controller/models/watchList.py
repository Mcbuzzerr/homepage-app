from pydantic import BaseModel
from enum import Enum, IntEnum
from beanie import Document, PydanticObjectId
from typing import Optional


class MediaType(IntEnum):
    movie = 0
    series = 1


class MediaItem(BaseModel):
    index: str
    title: str
    type: MediaType  # change to enum, see https://pydantic-docs.helpmanual.io/usage/types/#enums
    services: list[str] = []
    year: Optional[int]
    rating: Optional[float]
    durationMinutes: Optional[int]  # Only for movies
    episodeCount: Optional[int]  # Only for series
    tags: list[str] = []

    def toJSON(self):
        string = (
            "{"
            + f'"index": "{self.index}", "title": "{self.title}", "type": {self.type}, "services": ['
            + ", ".join(self.services)
            + "], "
            + f'"year": {self.year}, "rating": {self.rating}, "durationMinutes": {self.durationMinutes}, "episodeCount": {self.episodeCount}, "tags": ['
            + ", ".join(self.tags)
            + "]"
            + "}"
        )
        return string


class WatchList(Document):
    id: Optional[PydanticObjectId]
    ownerId: Optional[PydanticObjectId]
    title: str
    index: Optional[int]
    mediaItems: list[MediaItem] = []

    def toJSON(self):
        def joinMediaItems(mediaItems):
            string = ""
            for item in mediaItems:
                string += item.toJSON() + ", "
            return string[:-2]

        string = (
            "{"
            + f'"id": "{self.id}", "ownerId": "{self.ownerId}", "title": "{self.title}", "index": {self.index}, "mediaItems": ['
            + joinMediaItems(self.mediaItems)
            + "]"
            + "}"
        )
        return string

from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
from models.profile import Profile, Profile_in
from models.watchList import WatchList, MediaItem, MediaType

import json
import asyncio
import confluent_kafka
from confluent_kafka import KafkaException, Producer

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# To enable prometheus metrics, uncomment the following lines and install the dependencies
from starlette_exporter import PrometheusMiddleware, handle_metrics

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)


def hyperLink(
    id: PydanticObjectId, resource: str, port: int = 80, domain: str = "localhost"
):
    return f"http://{domain}:{port}/{resource}/{id.__str__()}"


def receipt(self, err, msg):
    if err is not None:
        print("Failed to deliver message: {0}: {1}".format(msg.value(), err.str()))
    else:
        message = "Produced message on topic {0} with value of {1}".format(
            msg.topic(), msg.value().decode("utf-8")
        )
        print(message)


@app.on_event("startup")
async def startup():
    app.Producer = Producer({"bootstrap.servers": "homepage-broker:29092"})
    app.databaseClient = AsyncIOMotorClient(config("MONGO_URI"))
    await init_beanie(
        database=app.databaseClient.HomePage,
        document_models=[Profile, WatchList],
    )
    print("Connected to database")


# Routes


@app.get("/")
async def read_root():
    return {"Hello": "World"}


# CRUD operations for watchLists
# Create
@app.post("/watchList/create/{profileId}", status_code=201, tags=["WatchLists"])
async def create_WatchList(profileId: PydanticObjectId, watchList: WatchList):
    # Produce a new watchList to kafka for the database to create
    message = {"profileId": profileId.__str__(), "watchList": watchList.toJSON()}
    message = json.dumps(message).encode("utf-8")
    print(message)
    app.Producer.produce(
        "watchlists",
        message,
        "watchlist-create",
        callback=receipt,
    )
    return (
        watchList.id.__str__()
    )  # Replace with HATEOAS compliant link to watchList page (/watchList/{watchListId})


# Read
@app.get("/watchList/all", tags=["WatchLists"])
async def get_all_WatchLists():
    # Get all watchLists from the database - this is a read-only operation so no kafka
    watchLists = []
    async for watchList in WatchList.find():
        watchLists.append(watchList)
        watchList.ownerId = hyperLink(watchList.ownerId, "profile")
    return watchLists


@app.get("/watchList/{watchListId}", tags=["WatchLists"])
async def get_WatchList(watchListId: PydanticObjectId):
    # Get a watchList from the database - this is a read-only operation so no kafka
    watchList = await WatchList.get(watchListId)
    if watchList is None:
        raise HTTPException(status_code=404, detail="WatchList not found")
    watchList.ownerId = hyperLink(watchList.ownerId, "profile")
    return watchList


@app.get("/watchList/fromProfile/{profileId}", tags=["WatchLists"])
async def get_WatchList_fromProfile(profileId: PydanticObjectId):
    profile = await Profile.get(profileId)
    print(profile)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    print(profile.watchLists)
    if profile.watchLists == []:
        raise HTTPException(status_code=404, detail="Profile has no watchLists")
    watchLists = []
    async for watchList in WatchList.find({"_id": {"$in": profile.watchLists}}):
        watchLists.append(watchList)
    return watchLists


# Update
@app.put("/watchList/edit", tags=["WatchLists"])
async def edit_WatchList(watchListId: PydanticObjectId, watchList: WatchList):
    # Produce an edited watchList to kafka for the database to update
    watchList.id = watchListId
    encodedWatchList = watchList.toJSON().encode("utf-8")
    app.Producer.produce(
        "watchlists",
        encodedWatchList,
        "watchlist-update",
        callback=receipt,
    )
    return (
        watchList.id
    )  # Replace with HATEOAS compliant link to watchList page (/watchList/{watchListId})


@app.put("/watchList/{watchListId}/addMediaItem", tags=["WatchLists"])
async def add_MediaItem_to_WatchList(
    watchListId: PydanticObjectId, mediaItem: MediaItem
):
    # Produce a new mediaItem to kafka for the database to add to the watchList
    message = {
        "watchListId": watchListId.__str__(),
        "mediaItem": mediaItem.toJSON(),
    }
    message = json.dumps(message).encode("utf-8")
    app.Producer.produce(
        "watchlists",
        message,
        "watchlist-add-media-item",
        callback=receipt,
    )
    return watchListId


# Delete
@app.delete("/watchList/{watchListId}/delete", tags=["WatchLists"])
async def delete_WatchList(watchListId: PydanticObjectId):
    # Produce a delete event to kafka for the database to delete a watchList
    app.Producer.produce(
        "watchlists",
        watchListId.__str__().encode("utf-8"),
        "watchlist-delete",
        callback=receipt,
    )

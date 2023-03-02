from fastapi import FastAPI, Depends
from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
from models.profile import Profile, Profile_in
from models.watchList import WatchList, MediaItem, MediaType

import asyncio
import confluent_kafka
from confluent_kafka import KafkaException, Producer

app = FastAPI()


# To enable prometheus metrics, uncomment the following lines and install the dependencies
# from starlette_exporter import PrometheusMiddleware, handle_metrics

# app.add_middleware(PrometheusMiddleware)
# app.add_route("/metrics", handle_metrics)
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
@app.post("/watchlist/create", status_code=201, tags=["WatchLists"])
async def create_WatchList(watchList: WatchList):
    # Produce a new watchList to kafka for the database to create
    encodedWatchList = watchList.toJSON().encode("utf-8")
    print(encodedWatchList)
    app.Producer.produce(
        "watchlists",
        encodedWatchList,
        "watchlist-create",
        callback=receipt,
    )
    return (
        watchList.id
    )  # Replace with HATEOAS compliant link to watchList page (/watchList/{watchListId})


# Read
@app.get("/watchList/{watchListId}", tags=["WatchLists"], response_model=WatchList)
async def get_WatchList(watchListId: PydanticObjectId):
    # Get a watchList from the database - this is a read-only operation so no kafka
    return await WatchList.find_one({"id": watchListId})


# Update
@app.put("/watchList/edit", tags=["WatchLists"])
async def edit_WatchList(watchListId: PydanticObjectId, watchList: WatchList):
    # Produce an edited watchList to kafka for the database to update
    encodedWatchList = watchList.toJSON().encode("utf-8")
    app.Producer.produce(
        "watchLists",
        encodedWatchList,
        "watchList-update",
        callback=receipt,
    )
    return (
        watchList.id
    )  # Replace with HATEOAS compliant link to watchList page (/watchList/{watchListId})


# Delete
@app.delete("/watchList/{watchListId}/delete", tags=["WatchLists"])
async def delete_WatchList(watchListId: PydanticObjectId):
    # Produce a delete event to kafka for the database to delete a watchList
    app.Producer.produce(
        "watchLists",
        watchListId.__str__().encode("utf-8"),
        "watchList-delete",
        callback=receipt,
    )

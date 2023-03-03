import json
from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
from confluent_kafka import Consumer, KafkaException, KafkaError

from models.profile import Profile, Profile_in
from models.watchList import WatchList, MediaItem, MediaType
import asyncio

print("Starting profiles controller")
profileConsumer = Consumer(
    {
        "bootstrap.servers": "homepage-broker:29092",
        "group.id": "profiles-consumer",
        "auto.offset.reset": "earliest",
    }
)


async def start_server():
    print("Starting beanie")
    databaseClient = AsyncIOMotorClient(config("MONGO_URI"))
    await init_beanie(
        database=databaseClient.HomePage,
        document_models=[Profile, WatchList],
    )
    await consumeLoop(profileConsumer, ["profiles"])


async def consumeLoop(consumer, topics):
    print("Starting consumer loop")
    running = True
    try:
        print("Subscribing to topics: {}".format(topics))
        consumer.subscribe(["watchlists"])

        while running:
            msg = consumer.poll(1.0)
            print("Polling")
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(
                        "End of partition reached {0}/{1}".format(
                            msg.topic(), msg.partition()
                        )
                    )
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                print("Consumed message: {}".format(msg.value().decode("utf-8")))
                await handleMessage(msg)
    finally:
        consumer.close()


async def handleMessage(message: bytes):
    key = message.key().decode("utf-8")
    value = message.value().decode("utf-8")
    # ADD STATEMENT FOR watchlist-add-media-item that adds a media item to a watchlist
    if key == "watchlist-create":
        # Create a new watchList
        # Incoming JSON is no longer what these 3 lines of code expect, UPDATE
        jsonValue = json.loads(value)
        watchlist = WatchList(**jsonValue)
        await WatchList.save(watchlist)
        # Add watchlistID to profile
        print("Created watchlist")
    elif key == "watchlist-update":
        # Update an existing watchList
        jsonValue = json.loads(value)
        watchlist = WatchList.get(PydanticObjectId(jsonValue["id"]))
        watchlist = WatchList(**jsonValue)
        await WatchList.save(watchlist)
        print("Updated watchlist")
    elif key == "watchlist-delete":
        # Delete an existing watchList
        watchlist = await WatchList.get(PydanticObjectId(value))
        await watchlist.delete()
        print("Deleted watchlist")
    else:
        print("Unknown message key: {}".format(key))


asyncio.run(start_server())

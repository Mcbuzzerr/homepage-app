import json
from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
from confluent_kafka import Consumer, KafkaException, KafkaError
from prometheus_client import start_http_server
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
    print("Started beanie")
    print("Starting metrics server")
    start_http_server(8000)
    print("Started metrics server")
    await consumeLoop(profileConsumer, ["watchlists"])


async def consumeLoop(consumer, topics):
    print("Starting consumer loop")
    running = True
    try:
        print("Subscribing to topics: {}".format(topics))
        consumer.subscribe(topics)

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
                print("Processing message:")
                print("Key: {}".format(msg.key().decode("utf-8")))
                print("Consumed message: {}".format(msg.value().decode("utf-8")))
                await handleMessage(msg)
    finally:
        consumer.close()


async def handleMessage(message: bytes):
    key = message.key().decode("utf-8")
    value = message.value().decode("utf-8")
    match key:
        case "watchlist-create":
            await watchlist_create(value)
        case "watchlist-update":
            await watchlist_update(value)
        case "watchlist-delete":
            await watchlist_delete(value)
        case "watchlist-add-media-item":
            await watchlist_add_media_item(value)
        case _:  # default
            print("Unknown message key: {}".format(key))


async def watchlist_add_media_item(value):
    print("Adding media item to watchlist")
    # Add a media item to a watchlist # UNTESTED
    jsonValue = json.loads(value)
    print(jsonValue)
    print(jsonValue["watchListId"])
    print(json.loads(jsonValue["mediaItem"]))
    watchlist = await WatchList.get(PydanticObjectId(jsonValue["watchListId"]))
    mediaItem = MediaItem(**json.loads(jsonValue["mediaItem"]))
    watchlist.mediaItems.append(mediaItem)
    await WatchList.save(watchlist)
    print("Added media item to watchlist")


async def watchlist_create(value):
    print("Creating watchlist")
    # Create a new watchList
    jsonValue = json.loads(value)
    profile = await Profile.get(PydanticObjectId(jsonValue["profileId"]))
    watchListJsonValue = json.loads(jsonValue["watchList"])
    watchListJsonValue["id"] = PydanticObjectId()
    watchListJsonValue["ownerId"] = profile.id
    watchlist = WatchList(**watchListJsonValue)
    await WatchList.save(watchlist)
    profile.watchLists.append(watchlist.id)
    await Profile.save(profile)
    # Add watchlistID to profile
    print("Created watchlist")


async def watchlist_update(value):
    print("Updating watchlist")
    # Update an existing watchList
    jsonValue = json.loads(value)
    jsonValue["id"] = PydanticObjectId(jsonValue["id"])
    watchlist = await WatchList.get(PydanticObjectId(jsonValue["id"]))

    if jsonValue["ownerId"] == "None":
        jsonValue["ownerId"] = watchlist.ownerId
    if jsonValue["title"] == "None":
        jsonValue["title"] = watchlist.title
    if jsonValue["index"] == "None":
        jsonValue["index"] = watchlist.index
    if jsonValue["mediaItems"] == "None":
        jsonValue["mediaItems"] = watchlist.mediaItems

    watchlist = WatchList(**jsonValue)
    await WatchList.save(watchlist)
    print("Updated watchlist")


async def watchlist_delete(value):
    print("Deleting watchlist")
    # Delete an existing watchList
    watchlist = await WatchList.get(PydanticObjectId(value))
    account = await Profile.get(watchlist.ownerId)
    account.watchLists.remove(watchlist.id)
    await Profile.save(account)
    await watchlist.delete()
    print("Deleted watchlist")


asyncio.run(start_server())

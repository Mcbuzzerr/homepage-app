import json
from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
from confluent_kafka import Consumer, KafkaException

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

        consumer.subscribe(["profiles"])

        while running:
            msg = consumer.poll(1.0)
            print("Polling")
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
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
    if key == "profile-create":
        # Create a new profile
        jsonValue = json.loads(value)
        profile = Profile(**jsonValue)
        await Profile.save(profile)
        print("Created profile")
        pass
    elif key == "profile-update":
        # Update an existing profile
        jsonValue = json.loads(value)
        profile = Profile.get(PydanticObjectId(jsonValue["id"]))
        profile = Profile(**jsonValue)
        await Profile.save(profile)
        print("Updated profile")
        pass
    elif key == "profile-delete":
        # Delete an existing profile
        profile = await Profile.get(PydanticObjectId(value))
        await profile.delete()
        print("Deleted profile")
        pass
    else:
        print("Unknown message key: {}".format(key))


asyncio.run(start_server())

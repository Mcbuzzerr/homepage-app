from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
from models.profile import Profile, Profile_in
from models.watchList import WatchList, MediaItem, MediaType

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


# CRUD operations for profiles
# Create
@app.post("/register", status_code=201, tags=["Profiles"])
async def register_Profile(profile: Profile_in):
    # Produce a new profile to kafka for the database to create
    newProfile = Profile(id=PydanticObjectId(), **profile.dict())
    print(newProfile)
    encodedProfile = newProfile.toJSON().encode("utf-8")
    print(encodedProfile)
    app.Producer.produce(
        "profiles",
        encodedProfile,
        "profile-create",
        callback=receipt,
    )
    return (
        newProfile.id
    )  # Replace with HATEOAS compliant link to profile page (/profile/{profileId})


# Read
@app.get("/profile/all", tags=["Profiles"])
async def get_Profiles():
    # Get all profiles from the database - this is a read-only operation so no kafka
    profiles = []
    async for profile in Profile.find_all():
        new_watchLists = []
        for watchList in profile.watchLists:
            new_watchLists.append(hyperLink(watchList, "watchList"))
        profile.watchLists = new_watchLists
        profiles.append(profile)
    return profiles


@app.get("/profile/{profileId}", tags=["Profiles"], response_model=Profile)
async def get_Profile(profileId: PydanticObjectId):
    # Get a profile from the database - this is a read-only operation so no kafka
    profile = await Profile.get(profileId)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    profile.id = hyperLink(profile.id, "profile")

    new_watchLists = []
    for watchList in profile.watchLists:
        new_watchLists.append(hyperLink(watchList, "watchList"))
    profile.watchLists = new_watchLists

    return profile


# Update
@app.put("/profile/{profileId}/edit", tags=["Profiles"])
async def edit_Profile(profileId: PydanticObjectId, profile: Profile_in):
    # Produce an edited profile to kafka for the database to update
    newProfile = Profile(id=profileId, **profile.dict())
    encodedProfile = newProfile.toJSON().encode("utf-8")
    app.Producer.produce(
        "profiles",
        encodedProfile,
        "profile-update",
        callback=receipt,
    )
    return (
        newProfile.id
    )  # Replace with HATEOAS compliant link to profile page (/profile/{profileId})


# Delete
@app.delete("/profile/{profileId}/delete", tags=["Profiles"])
async def delete_Profile(profileId: PydanticObjectId):
    # Produce a delete event to kafka for the database to delete a profile
    app.Producer.produce(
        "profiles",
        profileId.__str__().encode("utf-8"),
        "profile-delete",
        callback=receipt,
    )

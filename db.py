from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb+srv://enriquecapellan:Capellan2907@cluster0.p2hqd.mongodb.net/blindlight"

client: AsyncIOMotorClient = None


async def get_db_client() -> AsyncIOMotorClient:
    return client


async def connect_db():
    global client
    client = AsyncIOMotorClient(MONGO_DETAILS)


async def close_db():
    client.close()


def get_collection(collection: str):
    database = client.blindlight
    collection = database.get_collection(collection)
    return collection

# helpers


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "password": user["password"],
        "username": user["username"],
        "type": user["type"],
    }


# user
async def get_users():
    users = []
    async for user in get_collection('users').find():
        users.append(user_helper(user))
    return users


async def get_user(id: str) -> dict:
    user = await get_collection('users').find_one({"_id": ObjectId(id)})
    if(user):
        return user_helper(user)


async def get_user_by_username(username: str) -> dict:
    user = await get_collection('users').find_one({"username": username})
    if(user):
        return user_helper(user)


async def create_user(data: dict) -> dict:
    users_collection = get_collection('users')
    user = await users_collection.insert_one(data)
    new_user = await users_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


async def update_user(id: str, data: dict) -> dict:
    users_collection = get_collection('users')
    if len(data) < 1:
        return False
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await users_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if update_user:
            return user_helper(update_user)
        return False


async def delete_user(id: str):
    users_collection = get_collection('users')
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        await users_collection.delete_one({"_id": ObjectId(id)})
        return True

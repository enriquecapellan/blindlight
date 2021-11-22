import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb+srv://enriquecapellan:Capellan2907@cluster0.p2hqd.mongodb.net/blindlight"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.blindlight

users_collection = database.get_collection("users")

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
    async for user in users_collection.find():
        users.append(user_helper(user))
    return users


async def get_user(id: str) -> dict:
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if(user):
        return user_helper(user)


async def get_user_by_username(username: str) -> dict:
    user = await users_collection.find_one({"username": username})
    if(user):
        return user_helper(user)


async def create_user(data: dict) -> dict:
    user = await users_collection.insert_one(data)
    new_user = await users_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


async def update_user(id: str, data: dict) -> dict:
    if len(data) < 1:
        return False
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await users_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        if update_user:
            return user_helper(update_user)
        return False


async def delete_user(id: str):
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if user:
        await users_collection.delete_one({"_id": ObjectId(id)})
        return True

"""
Structure of collection:

LOGIN_COLLECTION
{
    username: string,
    password: string
}

IMAGE_COLLECTION
{
    "title": title,
    "creator": username,
    "image": image,
    "likes": 0,
    "comments": [
        {
            "username": string,
            "content": string
        }
    ]
}

"""
from pymongo import MongoClient

DATABASE_NAME = "NotPixar"

mongo_client = MongoClient("localhost", 27017)
database = mongo_client["NotPixar"]
login_collection = database["login"]
image_collection = database["images"]

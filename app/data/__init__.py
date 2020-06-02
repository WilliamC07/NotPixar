"""
Structure of collection:

LOGIN_COLLECTION
{
    username: string,
    password: string
}

IMAGE_COLLECTION
{
    username: string,
    title: string,
    ppm: string,
}

"""
from pymongo import MongoClient

DATABASE_NAME = "NotPixar"

mongo_client = MongoClient("localhost", 27017)
database = mongo_client["NotPixar"]
login_collection = database["login"]
image_collection = database["images"]

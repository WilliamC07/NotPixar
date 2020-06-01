"""
Structure of collection:

LOGIN_COLLECTION
{
    username: string,
    password: string
}

"""
from pymongo import MongoClient

DATABASE_NAME = "NotPixar"

mongo_client = MongoClient("localhost", 27017)
database = mongo_client["NotPixar"]
login_collection = database["login"]

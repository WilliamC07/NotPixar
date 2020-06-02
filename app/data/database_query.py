from data import login_collection, image_collection
from bson import ObjectId
from typing import Dict

def is_valid_login(username: str, password: str) -> bool:
    return login_collection.find_one({"username": username, "password": password}) is not None


def does_username_exist(username: str) -> bool:
    return login_collection.find_one({"username": username}) is not None


def create_account(username: str, password: str):
    login_collection.insert_one({"username": username, "password": password})


def store_image(title: str, image: str, username: str) -> str:
    return str(image_collection.insert_one({
        "title": title,
        "creator": username,
        "image": image,
        "likes": 0,
        "comments": []
    }).inserted_id)

def get_image(id: str) -> Dict:
    image_details = image_collection.find_one({
        "_id": ObjectId(id)
    })

    if image_details is None:
        return None

    # don't need to send _id since the frontend already knows it (in url)
    del image_details["_id"]
    return image_details

from data import login_collection, image_collection
from bson import ObjectId
from typing import Dict, List

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

def add_comment(art_id: str, content: str, username: str):
    image_collection.find_one_and_update(
        {"_id": ObjectId(art_id)},
        {"$push": {"comments": {"username": username, "content": content}}})

def get_all_art() -> List:
    images = list(image_collection.find({}))
    for image in images:
        image["art_id"] = str(image["_id"])
        del image["_id"]
        image["num_comments"] = len(image["comments"])
        del image["comments"]
    return images

from flask import Blueprint, render_template, request, session
from data import database_query
from PIL import Image

api = Blueprint("api", __name__)

@api.route("/image/create", methods=["POST"])
def api_image_create():
    print("hello")
    art_information = request.get_json()
    title = art_information["title"]
    image = art_information["image"]
    # art_id = database_query.store_image(title, image, session["username"])
    art_id = database_query.store_image(title, image, "mario")
    return {
        "id": art_id
    }
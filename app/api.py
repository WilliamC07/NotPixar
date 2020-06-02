from flask import Blueprint, render_template, request, session
from data import database_query
from PIL import Image

api = Blueprint("api", __name__)

@api.route("/image/create", methods=["POST"])
def api_image_create():
    art_information = request.get_json()
    title = art_information["title"]
    ppm = art_information["ppm"]
    art_id = database_query.store_image(title, ppm, session["username"])
    return {
        "id": art_id
    }
from flask import Blueprint, request, session, flash, redirect, url_for
from data import database_query

api = Blueprint("api", __name__)

@api.route("/image/create", methods=["POST"])
def api_image_create():
    if "username" not in session:
        return "No permission", 403
    art_information = request.get_json()
    title = art_information["title"]
    image = art_information["image"]
    art_id = database_query.store_image(title, image, session["username"])
    return {
        "id": art_id
    }

@api.route("/comment/create", methods=["POST"])
def api_comment_create():
    if "username" not in session:
        return "No permission", 403
    comment_information = request.get_json()
    art_id = comment_information["art_id"]
    content = comment_information["content"]
    database_query.add_comment(art_id, content, session["username"])
    return ""

@api.route("/<string:id>/like", methods=["POST"])
def api_image_like(id: str):
    if "username" not in session:
        flash("Please login to like artwork", "danger")
        return redirect('/login')
    if database_query.did_user_like(session["username"], id):
        # unlike
        database_query.unlike_artwork(id, session["username"])
    else:
        database_query.like_artwork(id, session["username"])
    return "", 200

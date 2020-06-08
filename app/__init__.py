from flask import Flask, session, render_template, redirect, url_for, request, flash
from data import database_query
import os, random
from api import api

app = Flask(__name__)
app.secret_key = "NotPixar"
app.register_blueprint(api, url_prefix='/api')

@app.route("/")
def home():
    images = database_query.get_all_art()
    return render_template("home.html", images=images)

@app.route("/create-account", methods=["POST", "GET"])
def create_account():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_repeat = request.form["password_repeat"]

        if password != password_repeat:
            flash("Passwords do not match", "danger")
        elif len(password.strip()) == 0:
            flash("Passwords must not be blank", "danger")
        elif len(username.strip()) == 0:
            flash("Username must not be blank", "danger")
        elif database_query.does_username_exist(username):
            flash("Username already exists", "danger")
        else:
            database_query.create_account(username, password)
            session["username"] = username
            return redirect(url_for("home"))

        if "username" in session:
            # Logged in user cannot create an account
            return redirect(url_for("home"))

    return render_template("create-account.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if database_query.is_valid_login(username, password):
            session["username"] = username
            flash("You logged in", "success")
            return redirect(url_for("home"))
        else:
            flash("Wrong username or password", "danger")

    if "username" in session:
        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    flash("You logged out", "success")
    return redirect(url_for("login"))

@app.route("/create-art", methods=["GET"])
def create():
    if session:
        return render_template("create-art.html")
    else:
        flash("Login or create an account to begin drawing", "success")
        return redirect(url_for("login"))

@app.route("/view-art/<string:id>", methods=["GET"])
def art(id: str):
    image_details = database_query.get_image(id)
    if image_details is None:
        flash("Art does not exist!", "danger")
        return redirect(url_for("home"))
    comments_demo = [ {'username': "ethan", 'content': "looking snaggilicious"},{'username': "william", 'content': "dope!"}]
    if image_details is None:
        flash("Image does not exist!", "danger")
        return redirect(url_for("home"))
    return render_template("view-art.html", title=image_details["title"], creator=image_details["creator"],
                           image=image_details["image"], comments=image_details["comments"], comments_demo = comments_demo,
                           likes=image_details["likes"])

@app.route("/profile/<string:username>", methods=["GET"])
def user(username: str):
    return render_template("profile.html")


if __name__ == "__main__":
    app.debug = True
    app.run()

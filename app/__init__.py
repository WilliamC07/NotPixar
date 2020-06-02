from flask import Flask, session, render_template, redirect, url_for, request, flash
from data import database_query
import os, random
from api import api

app = Flask(__name__)
app.secret_key = "NotPixar"
app.register_blueprint(api, url_prefix='/api')

@app.route("/")
def home():
    images = [[
        "https://vignette.wikia.nocookie.net/symbolism/images/4/43/Orange.png/revision/latest?cb=20140818120046",
        "https://lh3.googleusercontent.com/proxy/8z88n9F4EFilgy7D9bRzF5dxCTbDL68w01SwL2VdYPohr7OxQUxdb16h3mG9vfaol7t4wgOaKeOQCSG2J2LLnqRV1Otb",
        "https://webkit.org/blog-files/color-gamut/Webkit-logo-sRGB.png",
        "https://www.iep.utm.edu/wp-content/media/blue.gif"
    ], [
        "https://colibriwp.com/blog/wp-content/uploads/2019/09/turquoise-1.jpg",
        "https://images-na.ssl-images-amazon.com/images/I/21AoJYAb5lL._AC_SX425_.jpg",
        "https://cdn-3d.niceshops.com/upload/image/product/large/default/vallejo-game-color-bald-moon-yellow-17-ml-279473-en.jpg"
    ], [
        "https://i1.wp.com/www.hisour.com/wp-content/uploads/2018/04/Blush-color.jpg?fit=720%2C720&ssl=1",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRdhQCbLnGyjN8528xlVPSpirT6dB-dtOOiZ3hbSZIsfrcY6gEu&usqp=CAU",
        "https://www.solidbackgrounds.com/images/2560x1440/2560x1440-gray-solid-color-background.jpg"
    ]]
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
    return render_template("create-art.html")

@app.route("/view-art/<string:id>", methods=["GET"])
def art(id: str):
    return render_template("view-art.html")

@app.route("/profile/<string:username>", methods=["GET"])
def user(username: str):
    return render_template("profile.html")


if __name__ == "__main__":
    app.debug = True
    app.run()

from flask import Flask, session, render_template, redirect, url_for, request, flash
import os, random

app = Flask(__name__)

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


if __name__ == "__main__":
    app.debug = True
    app.run()
import unittest
import json
from contextlib import contextmanager

from flask import template_rendered

from data import database_creator
from __init__ import app

@contextmanager
def captured_templates(app):
    """
    https://stackoverflow.com/a/40531281/7154700
    :param app:
    :return:
    """
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

class Test(unittest.TestCase):
    def setUp(self) -> None:
        # run every time we run a test case
        app.testing = True
        self.app = app.test_client()
        database_creator.recreate_database()

    def login(self, username: str, password: str):
        return self.app.post("/login", data={
            "username": username,
            "password": password
        }, follow_redirects=True)

    def logout(self):
        return self.app.get("/logout", follow_redirects=True)

    def create_account(self, username: str, password: str):
        return self.app.post("/create-account", data={
            "username": username,
            "password": password,
            "password_repeat": password,
        }, follow_redirects=True)

    def test_login(self):
        # create account
        username = "username123"
        password = "password123"
        self.create_account(username, password)
        self.login(username, password)
        with self.app as c:
            with c.session_transaction() as session:
                # make sure session knows you are logged in
                self.assertEqual(session["username"], username)
        self.logout()
        with self.app as c:
            with c.session_transaction() as session:
                # make sure session knows you are logged in
                self.assertFalse("username" in session)

    def test_create_art(self):
        username = "username123"
        password = "password123"
        self.create_account(username, password)
        self.login(username, password)

        image_details = {
            "title": "test art 123",
            "image": "P3 3 2 255 255 0 0 0 255 0 0 0 255 255 255 0 255 255 255 0 0 0"
        }

        response = self.app.post("/api/image/create", json=image_details)
        art_id = json.loads(response.get_data(as_text=True))["id"]

        # the server will add these details
        image_details["creator"] = username
        image_details["likes"] = 0
        image_details["comments"] = []

        with captured_templates(app) as templates:
            self.app.get("/view-art/" + art_id)
            template, context = templates[0]

            for key, val in image_details.items():
                self.assertEqual(val, context[key])

    def test_create_comment(self):
        username = "artowner"
        password = "artowner"
        self.create_account(username, password)
        self.login(username, password)

        image_details = {
            "title": "test art 123",
            "image": "P3 3 2 255 255 0 0 0 255 0 0 0 255 255 255 0 255 255 255 0 0 0"
        }

        response = self.app.post("/api/image/create", json=image_details)
        art_id = json.loads(response.get_data(as_text=True))["id"]

        # the server will add these details
        image_details["creator"] = username
        image_details["likes"] = 0

        self.logout()

        username = "commentowner"
        password = "commentowner"
        self.create_account(username, password)
        self.login(username, password)
        self.app.post("/api/comment/create", json={"art_id": art_id, "content": "this is the comment"})

        with captured_templates(app) as templates:
            self.app.get("/view-art/" + art_id)
            template, context = templates[0]

            self.assertDictEqual({
                "content": "this is the comment",
                "username": username
            }, context["comments"][0])

    def test_likes(self):
        username = "artowner"
        password = "artowner"
        self.create_account(username, password)
        self.login(username, password)

        image_details = {
            "title": "test art 123",
            "image": "P3 3 2 255 255 0 0 0 255 0 0 0 255 255 255 0 255 255 255 0 0 0"
        }

        response = self.app.post("/api/image/create", json=image_details)
        art_id = json.loads(response.get_data(as_text=True))["id"]

        # the server will add these details
        image_details["creator"] = username
        image_details["likes"] = 0

        self.logout()

        username = "liker"
        password = "liker"
        self.create_account(username, password)
        self.login(username, password)

        self.app.post(f"/api/{art_id}/like")
        with captured_templates(app) as templates:
            self.app.get("/view-art/" + art_id)
            template, context = templates[0]

            self.assertEqual(1, context["likes"])
            self.assertTrue(context["hasLiked"])

        #unlike
        self.app.post(f"/api/{art_id}/like")
        with captured_templates(app) as templates:
            self.app.get("/view-art/" + art_id)
            template, context = templates[0]

            self.assertEqual(0, context["likes"])
            print(context)
            self.assertFalse(context["hasLiked"])



if __name__ == "__main__":
    unittest.main()
    database_creator.recreate_database()

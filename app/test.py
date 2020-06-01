import unittest
from __init__ import app
from data import database_creator
import json
from flask import template_rendered
from contextlib import contextmanager
import pprint

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


if __name__ == "__main__":
    unittest.main()
    database_creator.recreate_database()

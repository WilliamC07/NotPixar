import sqlite3

connection = sqlite3.connect("database.db", check_same_thread=False)
cursor = connection.cursor()

table_names = [
    "users",
    "arts",
    "comments",
    "likes"
]

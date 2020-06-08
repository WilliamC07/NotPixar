import sqlite3

cursor = sqlite3.connect("database.db", check_same_thread=False).cursor()

table_names = [
    "users",
    "arts",
    "comments",
    "likes"
]

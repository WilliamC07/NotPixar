from data import cursor
from typing import Dict, List

def is_valid_login(username: str, password: str) -> bool:
    cursor.execute("SELECT username FROM users WHERE username = ? AND password = ?", (username, password))
    return cursor.fetchone() is not None

def does_username_exist(username: str) -> bool:
    cursor.execute("SELECT username FROM users where username = ?", (username, ))
    return cursor.fetchone() is not None

def create_account(username: str, password: str):
    cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))

def store_image(title: str, image: str, username: str) -> str:
    cursor.execute('''
    INSERT INTO arts (
        title, 
        creator, 
        likes, 
        image
    )
    VALUES (?, ?, ?, ?)''', (title, username, 0, image))
    return str(cursor.lastrowid)

def get_image(id: str) -> Dict:
    cursor.execute("SELECT title, creator, likes, image FROM arts WHERE id = ?", (id,))
    data = cursor.fetchone()
    image = {
        "title": data[0],
        "creator": data[1],
        "image": data[3],
        "likes": int(data[2]),
        "comments": []
    }
    cursor.execute("SELECT username, content from comments WHERE artID = ?", (id, ))
    for comment in cursor.fetchall():
        image["comments"].append({
            "username": comment[0],
            "content": comment[1]
        })
    return image

def add_comment(art_id: str, content: str, username: str):
    cursor.execute("INSERT INTO comments (username, content, artID) VALUES (?, ?, ?)", (username, content, art_id))
    print('added comment for ' + art_id)

def get_all_art() -> List:
    images = []

    cursor.execute("SELECT id, title, likes, creator, image from arts")
    for art in cursor.fetchall():
        cursor.execute("SELECT COUNT(*) from comments where artID = ?", (art[0], ))

        images.append({
            "image": art[4],
            "likes": art[2],
            "creator": art[3],
            "title": art[1],
            "art_id": str(art[0]),
            "num_comments": cursor.fetchone()[0]
        })
    return images

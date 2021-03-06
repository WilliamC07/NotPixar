from typing import Dict, List

from data import cursor, connection

def is_valid_login(username: str, password: str) -> bool:
    cursor.execute("SELECT username FROM users WHERE username = ? AND password = ?", (username, password))
    connection.commit()
    return cursor.fetchone() is not None

def does_username_exist(username: str) -> bool:
    cursor.execute("SELECT username FROM users where username = ?", (username, ))
    connection.commit()
    return cursor.fetchone() is not None

def create_account(username: str, password: str):
    cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    connection.commit()

def store_image(title: str, image: str, username: str) -> str:
    cursor.execute('''
    INSERT INTO arts (
        title, 
        creator,
        image
    )
    VALUES (?, ?, ?)''', (title, username, image))
    connection.commit()
    return str(cursor.lastrowid)

def get_image(id: str, username: str) -> Dict:
    if username is None:
        username = ""

    cursor.execute("SELECT title, creator, image FROM arts WHERE id = ?", (id,))
    data = cursor.fetchone()
    if data is None:
        return None
    cursor.execute("SELECT COUNT(*) FROM likes where artID = ?", (int(id),))
    likes = int(cursor.fetchone()[0])
    image = {
        "title": data[0],
        "creator": data[1],
        "image": data[2],
        "likes": likes,
        "comments": [],
        "hasLiked": did_user_like(username, id)
    }
    cursor.execute("SELECT username, content from comments WHERE artID = ?", (id, ))
    for comment in cursor.fetchall():
        image["comments"].append({
            "username": comment[0],
            "content": comment[1]
        })
    connection.commit()
    return image

def did_user_like(username: str, art_id: str):
    if username is None:
        username = ""
    cursor.execute("SELECT * FROM likes WHERE username = ? AND artID = ?", (username, int(art_id)))
    connection.commit()
    return cursor.fetchone() is not None

def add_comment(art_id: str, content: str, username: str):
    cursor.execute("INSERT INTO comments (username, content, artID) VALUES (?, ?, ?)", (username, content, art_id))
    connection.commit()

def like_artwork(art_id: str, username: str):
    cursor.execute("INSERT INTO likes VALUES (?, ?)", (username, art_id))
    connection.commit()

def get_all_art(username: str) -> List:
    images = []
    if username is None:
        username = ""

    cursor.execute("SELECT id, title, creator, image from arts")
    for art in cursor.fetchall():
        cursor.execute("SELECT COUNT(*) from comments where artID = ?", (art[0], ))
        num_comments = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM likes where artID = ?", (art[0],))
        likes = int(cursor.fetchone()[0])

        images.append({
            "image": art[3],
            "likes": likes,
            "creator": art[2],
            "title": art[1],
            "art_id": str(art[0]),
            "num_comments": num_comments,
            "hasLiked": did_user_like(username, art[0])
        })
    connection.commit()
    return images

def unlike_artwork(art_id: str, username: str):
    cursor.execute("DELETE FROM likes WHERE artID = ? AND username = ?", (art_id, username))
    connection.commit()

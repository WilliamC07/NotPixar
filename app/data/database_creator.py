from data import cursor, table_names

def create_users_table():
    cursor.execute('''
    CREATE TABLE users(
        username TEXT NOT NULL unique,
        password TEXT
    )
    ''')

def create_art_table():
    cursor.execute('''
    CREATE TABLE arts(
        id INTEGER PRIMARY KEY,
        title TEXT,
        creator TEXT,
        image TEXT,
        FOREIGN KEY(creator) REFERENCES users(username)
    )
    ''')

def create_comment_table():
    cursor.execute('''
    CREATE TABLE comments(
        username TEXT,
        content TEXT,
        artID INTEGER,
        FOREIGN KEY(username) REFERENCES users(username),
        FOREIGN KEY(artID) REFERENCES arts(id)
    )
    ''')

def create_like_table():
    cursor.execute('''
    CREATE TABLE likes(
        username text,
        artID INTEGER,
        FOREIGN KEY(username) REFERENCES users(username),
        FOREIGN KEY(artID) REFERENCES arts(id)
    )
    ''')

def create_admin_account():
    cursor.execute('''
    INSERT INTO users VALUES(
        'admin',
        'admin' 
    )
    ''')

def recreate_database():
    # Clear all the tables
    statement = "DROP TABLE IF EXISTS "
    for table_name in table_names:
        cursor.execute(statement + table_name)

    # recreate the tables
    create_users_table()
    create_art_table()
    create_comment_table()
    create_like_table()

    create_admin_account()

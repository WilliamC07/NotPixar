from data import mongo_client, database, login_collection, DATABASE_NAME

def create_admin_account():
    login_collection.insert_one({
        "username": "admin",
        "password": "admin"
    })


def recreate_database():
    # Drop the mongo database if it exists
    if DATABASE_NAME in mongo_client.list_database_names():
        mongo_client.drop_database(DATABASE_NAME)

    create_admin_account()

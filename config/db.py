from pymongo import MongoClient

from dotenv import dotenv_values

config = dotenv_values(".env")


def connect_mongodb(app) :
    app.mongodb_client = MongoClient(config["MONGOURI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    return "db connected sucessfully"
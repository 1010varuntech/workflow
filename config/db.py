from pymongo import MongoClient


def connect_mongodb(app) :
    app.mongodb_client = MongoClient("mongodb+srv://varun:varun@cluster0.lsfxn8q.mongodb.net/")
    app.database = app.mongodb_client["appName=techStackStaging"]
    return "db connected sucessfully"
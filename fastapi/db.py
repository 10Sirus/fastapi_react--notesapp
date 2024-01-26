from pymongo import MongoClient
from bson import ObjectId
import hashlib
from passlib.context import CryptContext
import bcrypt

MONGO_URI="mongodb://localhost:27017"
client= MongoClient(MONGO_URI)
db =client["Notes"]
collection=db["notes"]
collection2=db["users"]

def create(data):
    data=dict(data)
    response=collection.insert_one(data)
    return str(response.inserted_id)

def all():
    response= collection.find({})
    data=[]
    for i in response:
        i["_id"]= str(i["_id"])
        data.append(i)
    return data

def get_one(condition):
    response= collection.find_one({"name":condition})
    if response is not None and "_id" in response:
        response["_id"] = str(response["_id"])
    else: 
        response= {"message": "noone with that name"}

    return response

def update(id,data):
    object_id = ObjectId(id)
    data=dict(data)
    response=collection.update_one({"_id":object_id}, {"$set": data})
    return response.modified_count
    


def delete(id):
    object_id = ObjectId(id)
    response=collection.delete_one({"_id":object_id})
    return response.deleted_count


# auth


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return pwd_context.hashed_password
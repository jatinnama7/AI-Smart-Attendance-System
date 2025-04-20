import bcrypt
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)
db = client['student_detail']
admin_collection = db['admin_credentials']

password = input("Enter a password for the admin account: ")
admin_email = input("Enter an email for the admin account: ")

hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

admin_collection.insert_one({
    "username": "admin",
    "password_hash": hashed,
    "email": admin_email
})
print("Admin account created successfully.")
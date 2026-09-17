import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER")

print("Username loaded:", bool(username))
print("Password loaded:", bool(password))
print("Cluster loaded:", bool(cluster))

if not username or not password or not cluster:
    print("MongoDB environment variables are missing!")
    exit()

uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority"

print("Testing MongoDB connection...")

try:
    client = MongoClient(
        uri,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=10000
    )

    client.admin.command("ping")

    print("MongoDB connection successful!")

except Exception as e:
    print("MongoDB connection failed:")
    print(e)
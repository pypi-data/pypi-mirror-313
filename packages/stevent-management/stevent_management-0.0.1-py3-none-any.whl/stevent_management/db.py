from dotenv import load_dotenv
load_dotenv()
import os
from pymongo import MongoClient


mongo_uri = os.getenv("CONN_STR")
if mongo_uri is None:
    raise ValueError("Mongo URI environment variable is not set.")

# Initialize the MongoDB client
client = MongoClient(mongo_uri)
db = client["Guests"]

# Define collections
profiler_collection = db["profiles"]
event_manager_collection = db["event_managers"]
event_collection = db["events"]
counters_collection = db["counters"]

# Test connection
try:
    client.admin.command("ping")
    print("Connected to MongoDB Atlas!")
except Exception as e:
    print(f"Connection failed: {e}")

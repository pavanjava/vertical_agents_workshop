# Get MongoDB connection string from environment
# Format: mongodb://username:password@localhost:27017/
import os
from agno.storage.mongodb import MongoDbStorage
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Create storage for sessions
mongo_agent_storage = MongoDbStorage(
    db_url=os.environ.get("mongo_url"),
    db_name=os.environ.get("database_name"),
    collection_name="agent_sessions"  # Collection name to use in the database for sessions
)


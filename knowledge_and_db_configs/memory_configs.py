# Create MongoDB memory database
import os
from typing import Any

from agno.memory.v2 import Memory
from agno.memory.v2.db.mongodb import MongoMemoryDb
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

memory_db: Any = MongoMemoryDb(
    db_url=os.environ.get("mongo_url"),
    db_name=os.environ.get("database_name"),
    collection_name="agent_memory"  # Collection name to use in the database
)

# Create memory instance with MongoDB backend
memory = Memory(db=memory_db)
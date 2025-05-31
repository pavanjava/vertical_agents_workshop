from agno.agent.agent import Agent
from agno.memory.db.base import MemoryDb
from agno.memory.v2.db.mongodb import MongoMemoryDb
from agno.memory.v2.memory import Memory
from agno.memory.v2.summarizer import SessionSummarizer
from agno.models.anthropic.claude import Claude
from dotenv import load_dotenv, find_dotenv
from rich.pretty import pprint

load_dotenv(find_dotenv())

mongo_url = "mongodb://localhost:27017/"
database_name = "vertical_agents"

# Create MongoDB memory database
memory_db:MemoryDb = MongoMemoryDb(
    db_url=mongo_url,
    db_name=database_name,
    collection_name="agent_memory"  # Collection name to use in the database
)

memory = Memory(
    db=memory_db,
    summarizer=SessionSummarizer(model=Claude(id="claude-3-7-sonnet-20250219")),
)

# Reset the memory for this example
memory.clear()

# No session and user ID is specified, so they are generated automatically
agent = Agent(
    model=Claude(id="claude-3-5-sonnet-20241022"),
    memory=memory,
    enable_user_memories=True,
    enable_session_summaries=True,
)

agent.print_response(
    "My name is John Doe and I like to hike in the mountains on weekends.",
    stream=True,
)

agent.print_response(
    "What are my hobbies?",
    stream=True,
)


memories = memory.get_user_memories()
print("John Doe's memories:")
pprint(memories)
session_summary = agent.get_session_summary()
pprint(session_summary)


# Now lets do a new session with a different user
session_id_2 = "1002"
mark_gonzales_id = "mark@example.com"

agent.print_response(
    "My name is Mark Gonzales and I like anime and video games.",
    stream=True,
    user_id=mark_gonzales_id,
    session_id=session_id_2,
)

agent.print_response(
    "What are my hobbies?",
    stream=True,
    user_id=mark_gonzales_id,
    session_id=session_id_2,
)


memories = memory.get_user_memories(user_id=mark_gonzales_id)
print("Mark Gonzales's memories:")
pprint(memories)

# We can get the session summary from memory as well
session_summary = memory.get_session_summary(
    session_id=session_id_2, user_id=mark_gonzales_id
)
pprint(session_summary)
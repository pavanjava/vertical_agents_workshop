from mem0 import Memory
from dotenv import load_dotenv, find_dotenv
from util.graph_viz import display_graph

load_dotenv(find_dotenv())

config = {
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o-mini",
            "temperature": 0.0,
            "max_tokens": 2000,
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-large",
            "embedding_dims": 1536
        }
    },
    "graph_store": {
        "provider": "memgraph",
        "config": {
            "url": "bolt://localhost:7687",
            "username": "memgraph",
            "password": "xxx"
        },
    }
}

# {
#     "provider": "neo4j",
#     "config": {
#         "url": "neo4j://localhost:7687",
#         "username": "neo4j",
#         "password": "neo4j@123"
#     },
# }

# {
#     "provider": "memgraph",
#     "config": {
#         "url": "bolt://localhost:7687",
#         "username": "memgraph",
#         "password": "xxx"
#     },
# }

m = Memory.from_config(config_dict=config)

# m.add("I like going to hikes", user_id="pavan123")
# m.add("I love to play badminton", user_id="pavan123")
# m.add("I hate playing badminton", user_id="pavan123")
# m.add("I have friend name sashank and he owns a organization called Antz.ai", user_id="pavan123")

# graph_resp = m.search("who own the organization?", user_id="pavan123")
# display_graph(data=graph_resp)
#
graph_resp = m.search("badminton is liked by?", user_id="pavan123")
display_graph(data=graph_resp)

import os
from mem0 import Memory
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": os.environ.get("QDRANT_COLLECTION"),
            "url": os.environ.get("QDRANT_URL"),
            "api_key": os.environ.get("QDRANT_API_KEY"),
            "embedding_model_dims": 1024,  # Change this according to your local model's dimensions
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "qwen3:14b",
            "temperature": 0,
            "max_tokens": 2000,
            "ollama_base_url": "http://localhost:11434",  # Ensure this URL is correct
        },
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "snowflake-arctic-embed2:latest",
            # Alternatively, you can use "snowflake-arctic-embed:latest"
            "ollama_base_url": "http://localhost:11434",
        },
    }
}

# Initialize Memory with the configuration
memory = Memory.from_config(config)

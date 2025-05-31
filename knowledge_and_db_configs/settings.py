import os
from typing import Dict, Any
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_qdrant_config() -> Dict[str, Any]:
    """
    Returns Qdrant configuration parameters.
    This avoids pickling issues by not creating the client instance here.

    Returns:
        Dict[str, Any]: Configuration parameters for Qdrant client
    """
    return {
        "url": str(os.environ.get("QDRANT_URL")),  # Ensure string type
        "api_key": str(os.environ.get("QDRANT_API_KEY")),  # Ensure string type
        "collection": "medical_knowledge", # collection to store the metadata and vectors
    }
# New Qdrant implementation for knowledge
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.qdrant import Qdrant

from knowledge_and_db_configs.settings import get_qdrant_config

medical_knowledge_base = PDFKnowledgeBase(
    path="../data/medical/",
    # use qdrant to retrieve the medical knowledge
    vector_db=Qdrant(
        **get_qdrant_config()
    )
)


legal_knowledge_base = PDFKnowledgeBase(
    path="../data/legal/",
    # use qdrant to retrieve the legal knowledge
    vector_db=Qdrant(
        **get_qdrant_config()
    )
)
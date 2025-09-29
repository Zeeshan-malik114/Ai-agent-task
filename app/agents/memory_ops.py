import os
import chromadb
from chromadb.config import Settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Ensure db directory exists
DB_DIR = "./db"
os.makedirs(DB_DIR, exist_ok=True)

# Initialize Chroma client
chroma_client = chromadb.PersistentClient(path=DB_DIR)

# Create or get collection
collection = chroma_client.get_or_create_collection("ai_assistant_memory")


def save_memory(text: str, contact: str, channel: str):
    try:
        memory_id = f"{contact}_{channel}_{len(collection.get()['ids']) + 1}"
        metadata = {"contact": contact, "channel": channel}
        collection.add(ids=[memory_id], documents=[text], metadatas=[metadata])
        logger.info(f"Memory saved for {contact} ({channel}): {text}")
    except Exception as e:
        logger.error(f"Failed to save memory for {contact}: {e}")


def search_memory(query: str, n_results: int = 3):
    try:
        results = collection.query(query_texts=[query], n_results=n_results)
        memories = results.get("documents", [[]])[0] if results else []
        metadatas = results.get("metadatas", [[]])[0] if results else []
        logger.info(f"Memory search for '{query}' returned {len(memories)} results")
        return {"documents": memories, "metadatas": metadatas}
    except Exception as e:
        logger.error(f"Failed to search memory: {e}")
        return {"documents": [], "metadatas": []}

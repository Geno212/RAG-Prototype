import chromadb
from chromadb.config import Settings as ChromaSettings
import asyncio
from typing import List, Dict, Any
import uuid
import logging

class VectorStore:
    async def add_documents(self, documents: List[Any], collection_name: str) -> None:
        pass

    async def search(self, query: str, collection_name: str, k: int = 4) -> Dict[str, Any]:
        pass

class ChromaDBStore(VectorStore):
    def __init__(self):
        self.client = chromadb.Client(ChromaSettings(persist_directory="./chroma_db"))
        self.lock = asyncio.Lock()
        self.logger = logging.getLogger(__name__)

    async def add_documents(self, documents: List[Any], collection_name: str) -> None:
        async with self.lock:
            collection = self.client.get_or_create_collection(collection_name)
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            ids = [str(uuid.uuid4()) for _ in documents]
            collection.add(documents=texts, metadatas=metadatas, ids=ids)

    async def search(self, query: str, collection_name: str, k: int = 4) -> Dict[str, Any]:
        async with self.lock:
            collection = self.client.get_collection(collection_name)
            results = collection.query(query_texts=[query], n_results=k)
            return {
                'documents': results['documents'],
                'metadatas': results['metadatas'],
                'distances': results['distances']
            }

    async def list_collections(self) -> List[str]:
        async with self.lock:
            collections = self.client.list_collections()
            return [collection.name for collection in collections]

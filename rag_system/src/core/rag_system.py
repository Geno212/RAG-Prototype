import aiofiles
from fastapi import UploadFile
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from typing import List, Dict, Any
import time
import asyncio
import logging
from pathlib import Path

class RAGSystem:
    def __init__(self, document_processor, vector_store, openai_api_key, model_name="gpt-3.5-turbo"):
        self.document_processor = document_processor
        self.vector_store = vector_store
        self.llm = ChatOpenAI(api_key=openai_api_key, model_name=model_name, temperature=0)
        self.chat_history: List[tuple] = []
        self.logger = logging.getLogger(__name__)
        self._system_prompt = self._create_system_prompt()

    def _create_system_prompt(self) -> str:
        return "You are a helpful AI assistant..."

    async def ingest_document(self, file: UploadFile, collection_name: str = "default_collection") -> None:
        temp_dir = Path("./temp_uploads")
        temp_dir.mkdir(exist_ok=True)
        file_path = temp_dir / file.filename
        contents = await file.read()
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(contents)
        documents = await asyncio.to_thread(self.document_processor.process_document, str(file_path))
        await self.vector_store.add_documents(documents, collection_name)
        file_path.unlink()

    async def query(self, question: str, collection_name: str = "default_collection") -> Dict[str, Any]:
        start_time = time.time()
        search_results = await self.vector_store.search(question, collection_name)
        context = "\n".join(search_results['documents'][0])
        messages = [SystemMessage(content=self._system_prompt), HumanMessage(content=f"Context: {context}\n\nQuestion: {question}")]
        response = await asyncio.to_thread(self.llm.predict_messages, messages)
        self.chat_history.append((question, response.content))
        return {
            'answer': response.content,
            'context': search_results['documents'][0],
            'processing_time': time.time() - start_time,
            'metadata': search_results['metadatas'][0]
        }

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader
)
from pathlib import Path
from typing import List, Dict, Any
import logging

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.logger = logging.getLogger(__name__)
        self._setup_loaders()

    def _setup_loaders(self):
        self.loaders: Dict[str, Any] = {
            '.pdf': PyPDFLoader,
            '.txt': TextLoader,
            '.docx': UnstructuredWordDocumentLoader,
            '.doc': UnstructuredWordDocumentLoader
        }

    def process_document(self, file_path: str) -> List[Any]:
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            extension = file_path.suffix.lower()
            if extension not in self.loaders:
                raise ValueError(f"Unsupported file type: {extension}")
            loader = self.loaders[extension](str(file_path))
            documents = loader.load()
            return self.text_splitter.split_documents(documents)
        except Exception as e:
            self.logger.error(f"Error processing document: {e}")
            raise

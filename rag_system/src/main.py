from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utils.config import get_settings
from src.core.document_processor import DocumentProcessor
from src.core.vector_store import ChromaDBStore
from src.core.rag_system import RAGSystem

# Define lifespan for app setup and cleanup
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.document_processor = DocumentProcessor(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )
    app.state.vector_store = ChromaDBStore()
    app.state.rag_system = RAGSystem(
        app.state.document_processor,
        app.state.vector_store,
        settings.OPENAI_API_KEY,
        settings.MODEL_NAME
    )
    yield
    await app.state.vector_store.cleanup()

app = FastAPI(title="RAG System API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include endpoint routes
from endpoints import upload_file, query, list_collections
app.include_router(upload_file.router)
app.include_router(query.router)
app.include_router(list_collections.router)

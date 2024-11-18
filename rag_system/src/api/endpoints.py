from fastapi import APIRouter, UploadFile, HTTPException, Depends
from fastapi import FastAPI, File
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from src.core.rag_system import RAGSystem

router = APIRouter()

class Query(BaseModel):
    question: str
    collection_name: Optional[str] = "default_collection"

class ResponseModel(BaseModel):
    answer: str
    context: List[str]
    processing_time: float
    metadata: List[Dict[str, Any]]

@router.post("/upload")
async def upload_file(
        file: UploadFile = File(...),
        collection_name: str = "default_collection",
        rag_system: RAGSystem = Depends(lambda: app.state.rag_system)
):
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        await rag_system.ingest_document(file, collection_name)
        return {"message": "Document uploaded and processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=ResponseModel)
async def query(
        query: Query,
        rag_system: RAGSystem = Depends(lambda: app.state.rag_system)
):
    try:
        result = await rag_system.query(query.question, query.collection_name)
        return ResponseModel(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/collections")
async def list_collections(
        vector_store = Depends(lambda: app.state.vector_store)
):
    try:
        collections = await vector_store.list_collections()
        return {"collections": collections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

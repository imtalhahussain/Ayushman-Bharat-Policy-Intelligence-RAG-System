# backend/app/api/routes_admin.py

from fastapi import APIRouter, UploadFile, File
from typing import List

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/upload-pdfs")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    # TODO: Save files to data/pdfs/ and trigger ingestion pipeline.
    filenames = [f.filename for f in files]
    return {"uploaded": filenames, "message": "Upload endpoint stub. Logic coming soon."}

@router.post("/reindex")
async def reindex():
    # TODO: call ingest_chunks() from rag.ingest
    # from backend.app.rag.ingest import ingest_chunks
    # ingest_chunks()
    return {"status": "ok", "message": "Reindex endpoint stub. Wire to ingest_chunks()."}

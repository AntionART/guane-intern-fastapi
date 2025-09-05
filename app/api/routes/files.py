"""File upload routes and worker status."""

import os
import uuid
from typing import Dict
from fastapi import APIRouter, UploadFile, File, HTTPException, status

from app.tasks.dog_tasks import get_worker_status

router = APIRouter()


@router.post("/files", response_model=Dict[str, str])
async def upload_file(file: UploadFile = File(...)):
    """Upload a file with any extension."""
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )
    
    # Create uploads directory if it doesn't exist
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    # Save file
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "saved_as": unique_filename,
            "size": len(content),
            "content_type": file.content_type or "unknown"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}"
        )


@router.get("/workers", response_model=Dict[str, str])
async def check_worker_status():
    """Check if Celery worker is functioning."""
    try:
        task = get_worker_status.delay()
        result = task.get(timeout=10)  # Wait up to 10 seconds
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Worker not available: {str(e)}"
        )
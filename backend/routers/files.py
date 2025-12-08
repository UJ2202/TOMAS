"""
Files Router

API endpoints for file upload and download operations.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from pathlib import Path
import uuid
import shutil

from core.database import get_db
from services.session_manager import SessionManager
from core.config import settings


router = APIRouter(prefix="/api/files", tags=["files"])


async def get_session_manager(db: AsyncSession = Depends(get_db)) -> SessionManager:
    """Get SessionManager instance"""
    return SessionManager(db)


@router.post("/upload/{session_id}")
async def upload_file(
    session_id: str,
    file: UploadFile = File(...),
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    Upload a file for a session

    Args:
        session_id: Session ID to associate file with
        file: File to upload

    Returns:
        File metadata including ID and path
    """
    # Validate session exists
    session = await session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    # Get session workspace
    workspace_path = Path(session.workspace_path)
    input_files_path = workspace_path / "input_files"
    input_files_path.mkdir(parents=True, exist_ok=True)

    # Generate unique filename
    file_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix
    unique_filename = f"{file_id}{file_extension}"
    file_path = input_files_path / unique_filename

    # Save file
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {str(e)}"
        )

    # Get file size
    file_size = file_path.stat().st_size

    # Check file size limit
    max_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if file_size > max_size:
        file_path.unlink()  # Delete the file
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {settings.MAX_UPLOAD_SIZE_MB}MB"
        )

    # Add file to session
    session_file = await session_manager.add_file(
        session_id=session_id,
        filename=unique_filename,
        original_filename=file.filename,
        file_path=str(file_path),
        file_size=file_size,
        mime_type=file.content_type,
        is_input=True
    )

    return {
        "file_id": session_file.id,
        "filename": session_file.filename,
        "original_filename": session_file.original_filename,
        "file_size": session_file.file_size,
        "mime_type": session_file.mime_type,
        "uploaded_at": session_file.uploaded_at.isoformat()
    }


@router.post("/upload-multiple/{session_id}")
async def upload_multiple_files(
    session_id: str,
    files: List[UploadFile] = File(...),
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    Upload multiple files for a session

    Args:
        session_id: Session ID to associate files with
        files: List of files to upload

    Returns:
        List of uploaded file metadata
    """
    uploaded_files = []

    for file in files:
        try:
            # Reuse single file upload logic
            result = await upload_file(session_id, file, session_manager)
            uploaded_files.append(result)
        except HTTPException as e:
            # Continue uploading other files even if one fails
            uploaded_files.append({
                "error": str(e.detail),
                "filename": file.filename
            })

    return {
        "uploaded_count": len([f for f in uploaded_files if "error" not in f]),
        "failed_count": len([f for f in uploaded_files if "error" in f]),
        "files": uploaded_files
    }


@router.get("/list/{session_id}")
async def list_session_files(
    session_id: str,
    is_input: bool = None,
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    List all files for a session

    Args:
        session_id: Session ID
        is_input: Filter by input (True) or output (False) files. None = all files

    Returns:
        List of file metadata
    """
    session = await session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    files = await session_manager.get_session_files(session_id, is_input)

    return {
        "session_id": session_id,
        "count": len(files),
        "files": [
            {
                "file_id": f.id,
                "filename": f.filename,
                "original_filename": f.original_filename,
                "file_size": f.file_size,
                "mime_type": f.mime_type,
                "is_input": f.is_input,
                "uploaded_at": f.uploaded_at.isoformat()
            }
            for f in files
        ]
    }


@router.get("/download/{session_id}/{file_id}")
async def download_file(
    session_id: str,
    file_id: str,
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    Download a specific file from a session

    Args:
        session_id: Session ID
        file_id: File ID to download

    Returns:
        File download response
    """
    session = await session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    # Get all session files
    files = await session_manager.get_session_files(session_id)
    session_file = next((f for f in files if f.id == file_id), None)

    if not session_file:
        raise HTTPException(status_code=404, detail=f"File {file_id} not found")

    file_path = Path(session_file.file_path)
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"File not found on disk: {session_file.file_path}"
        )

    return FileResponse(
        path=str(file_path),
        filename=session_file.original_filename,
        media_type=session_file.mime_type or "application/octet-stream"
    )


@router.delete("/{session_id}/{file_id}")
async def delete_file(
    session_id: str,
    file_id: str,
    session_manager: SessionManager = Depends(get_session_manager)
):
    """
    Delete a file from a session

    Args:
        session_id: Session ID
        file_id: File ID to delete

    Returns:
        Success message
    """
    session = await session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    # Get file
    files = await session_manager.get_session_files(session_id)
    session_file = next((f for f in files if f.id == file_id), None)

    if not session_file:
        raise HTTPException(status_code=404, detail=f"File {file_id} not found")

    # Delete from disk
    file_path = Path(session_file.file_path)
    if file_path.exists():
        try:
            file_path.unlink()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete file from disk: {str(e)}"
            )

    # Delete from database
    await session_manager.delete_file(file_id)

    return {
        "message": f"File {session_file.original_filename} deleted successfully",
        "file_id": file_id
    }

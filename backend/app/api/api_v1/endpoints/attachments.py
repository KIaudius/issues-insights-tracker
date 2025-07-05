from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from app.api.deps import get_db
from app.core.config import settings
from app.core.security import get_current_active_user
from app.crud.attachment_crud import get_attachment, get_attachments_by_issue, create_attachment, delete_attachment, save_upload_file, can_modify_attachment
from app.models.user import User
from app.schemas.attachment import AttachmentCreate, AttachmentResponse, AttachmentsResponse

router = APIRouter()

@router.get("/issue/{issue_id}", response_model=AttachmentsResponse)
async def read_attachments_by_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Retrieve attachments for an issue"""
    attachments, total = get_attachments_by_issue(
        db, 
        issue_id=issue_id,
        skip=skip, 
        limit=limit
    )
    return {
        "success": True,
        "data": attachments,
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit
    }

@router.post("/", response_model=AttachmentResponse, status_code=status.HTTP_201_CREATED)
async def create_attachment_endpoint(
    *,
    db: Session = Depends(get_db),
    issue_id: int = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Upload new attachment"""
    # Validate file size
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Maximum size is {settings.MAX_UPLOAD_SIZE / (1024 * 1024):.1f} MB"
        )
    
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower().lstrip('.')
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Save file
    try:
        file_path = await save_upload_file(file, issue_id)
        
        attachment_in = AttachmentCreate(
            filename=file.filename,
            content_type=file.content_type,
            size=file.size,
            issue_id=issue_id,
            file_path=file_path
        )
        
        attachment = create_attachment(db, attachment_in=attachment_in, uploader_id=current_user.id)
        return {"success": True, "data": attachment}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error uploading file: {str(e)}"
        )

@router.get("/{attachment_id}", response_model=AttachmentResponse)
async def read_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get attachment metadata by ID"""
    attachment = get_attachment(db, attachment_id=attachment_id)
    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found"
        )
    return {"success": True, "data": attachment}

@router.get("/{attachment_id}/download")
async def download_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Download attachment file"""
    attachment = get_attachment(db, attachment_id=attachment_id)
    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found"
        )
    
    file_path = os.path.join(settings.UPLOAD_DIR, attachment.file_path)
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on server"
        )
    
    return FileResponse(
        path=file_path,
        filename=attachment.filename,
        media_type=attachment.content_type
    )

@router.delete("/{attachment_id}", response_model=AttachmentResponse)
async def delete_attachment_endpoint(
    *,
    db: Session = Depends(get_db),
    attachment_id: int,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Delete attachment with permission check"""
    attachment = get_attachment(db, attachment_id=attachment_id)
    if not attachment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attachment not found"
        )
    
    # Check permissions
    if not can_modify_attachment(attachment, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    attachment = delete_attachment(db, attachment_id=attachment_id)
    return {"success": True, "data": attachment}

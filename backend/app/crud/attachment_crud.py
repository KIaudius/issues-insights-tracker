import os
import uuid
from typing import List, Optional, Tuple, BinaryIO

from sqlalchemy.orm import Session, joinedload
from fastapi import UploadFile

from app.models.attachment import Attachment
from app.models.user import User, UserRole
from app.core.config import settings
from app.schemas.attachment import AttachmentCreate

async def save_upload_file(upload_file: UploadFile, issue_id: int) -> str:
    """Save uploaded file to disk and return file path"""
    # Create issue directory if it doesn't exist
    issue_dir = os.path.join(settings.UPLOAD_DIR, f"issue_{issue_id}")
    os.makedirs(issue_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(upload_file.filename)[1] if upload_file.filename else ""
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(issue_dir, unique_filename)
    
    # Save file
    with open(file_path, "wb") as f:
        content = await upload_file.read()
        f.write(content)
    
    # Return relative path for storage in database
    return os.path.join(f"issue_{issue_id}", unique_filename)

def get_attachment(db: Session, attachment_id: int) -> Optional[Attachment]:
    """Get attachment by ID with uploader data"""
    return db.query(Attachment).options(joinedload(Attachment.uploader)).filter(Attachment.id == attachment_id).first()

def get_attachments_by_issue(
    db: Session, 
    issue_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> Tuple[List[Attachment], int]:
    """Get attachments for an issue with pagination"""
    query = db.query(Attachment).options(joinedload(Attachment.uploader)).filter(Attachment.issue_id == issue_id)
    
    # Get total count for pagination
    total = query.count()
    
    # Apply pagination
    attachments = query.order_by(Attachment.created_at.desc()).offset(skip).limit(limit).all()
    
    return attachments, total

def create_attachment(db: Session, attachment_in: AttachmentCreate, uploader_id: int) -> Attachment:
    """Create new attachment record"""
    db_attachment = Attachment(
        filename=attachment_in.filename,
        file_path=attachment_in.file_path,
        content_type=attachment_in.content_type,
        size=attachment_in.size,
        issue_id=attachment_in.issue_id,
        uploader_id=uploader_id
    )
    db.add(db_attachment)
    db.commit()
    db.refresh(db_attachment)
    return db_attachment

def delete_attachment(db: Session, attachment_id: int) -> Optional[Attachment]:
    """Delete attachment and file"""
    attachment = db.query(Attachment).filter(Attachment.id == attachment_id).first()
    if attachment:
        # Delete file from disk
        file_path = os.path.join(settings.UPLOAD_DIR, attachment.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete record from database
        db.delete(attachment)
        db.commit()
    return attachment

def can_modify_attachment(attachment: Attachment, user: User) -> bool:
    """Check if user can modify or delete attachment"""
    # Admin can modify any attachment
    if user.role == UserRole.ADMIN:
        return True
    
    # Maintainers can modify any attachment
    if user.role == UserRole.MAINTAINER:
        return True
    
    # Users can modify their own attachments
    return attachment.uploader_id == user.id

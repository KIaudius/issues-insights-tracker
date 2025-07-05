from typing import List, Optional
from datetime import datetime
from pydantic import Field, AfterValidator
from typing_extensions import Annotated
import re

from app.schemas.base import BaseSchema, BaseAPIResponse
from app.core.config import settings

# Custom validator functions
def validate_filename(v: str) -> str:
    """Validate and sanitize filename"""
    # Remove potentially dangerous characters
    safe_filename = re.sub(r'[^\w\.-]', '_', v)
    return safe_filename

def validate_file_extension(v: str) -> str:
    """Validate file extension is allowed"""
    ext = f".{v.split('.')[-1].lower()}" if '.' in v else ""
    if ext and ext not in settings.ALLOWED_UPLOAD_EXTENSIONS:
        raise ValueError(f"File extension {ext} is not allowed")
    return v

class AttachmentBase(BaseSchema):
    """Base schema for attachment data"""
    filename: Annotated[str, AfterValidator(validate_filename), AfterValidator(validate_file_extension)]
    content_type: str
    size: int

class AttachmentCreate(AttachmentBase):
    """Schema for creating an attachment"""
    issue_id: int
    file_path: str

class AttachmentInDB(AttachmentBase):
    """Schema for attachment data from database"""
    id: int
    issue_id: int
    uploader_id: int
    file_path: str
    created_at: datetime

class AttachmentWithUser(AttachmentInDB):
    """Schema for attachment with user data"""
    uploader: dict  # Simplified user info
    is_previewable: bool

class AttachmentResponse(BaseAPIResponse):
    """API response with attachment data"""
    data: AttachmentWithUser

class AttachmentsResponse(BaseAPIResponse):
    """API response with multiple attachments"""
    data: List[AttachmentWithUser]
    total: int
    page: int
    page_size: int

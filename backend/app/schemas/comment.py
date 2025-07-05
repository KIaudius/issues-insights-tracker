from typing import List, Optional
from datetime import datetime
from pydantic import Field, BeforeValidator
from typing_extensions import Annotated

from app.schemas.base import BaseSchema, BaseAPIResponse

# Custom validator functions
def clean_comment(v: str) -> str:
    """Clean and sanitize comment content"""
    # Basic sanitization - in a real app, use a proper HTML sanitizer
    return v.replace('<script>', '').replace('</script>', '')

class CommentBase(BaseSchema):
    """Base schema for comment data"""
    content: Annotated[str, BeforeValidator(clean_comment)] = Field(..., min_length=1)

class CommentCreate(CommentBase):
    """Schema for creating a comment"""
    issue_id: int

class CommentUpdate(CommentBase):
    """Schema for updating a comment"""
    pass

class CommentInDB(CommentBase):
    """Schema for comment data from database"""
    id: int
    issue_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class CommentWithUser(CommentInDB):
    """Schema for comment with user data"""
    user: dict  # Simplified user info

class CommentResponse(BaseAPIResponse):
    """API response with comment data"""
    data: CommentWithUser

class CommentsResponse(BaseAPIResponse):
    """API response with multiple comments"""
    data: List[CommentWithUser]
    total: int
    page: int
    page_size: int

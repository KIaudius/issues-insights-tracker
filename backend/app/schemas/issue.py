from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator, BeforeValidator
from typing_extensions import Annotated
from functools import partial

from app.models.issue import IssueSeverity, IssueStatus
from app.schemas.base import BaseSchema, BaseAPIResponse

# Custom validator functions
def clean_markdown(v: Optional[str]) -> Optional[str]:
    """Clean and sanitize markdown content"""
    if v is None:
        return v
    # Basic sanitization - in a real app, use a proper HTML sanitizer
    return v.replace('<script>', '').replace('</script>', '')

class IssueBase(BaseSchema):
    """Base schema for issue data"""
    title: str = Field(..., min_length=3, max_length=255)
    description: Annotated[str, BeforeValidator(clean_markdown)] = Field(..., min_length=10)
    severity: IssueSeverity = IssueSeverity.MEDIUM
    status: IssueStatus = IssueStatus.OPEN

class IssueCreate(IssueBase):
    """Schema for creating an issue"""
    assignee_id: Optional[int] = None
    
    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate that title is not empty or just whitespace"""
        if not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

class IssueUpdate(BaseSchema):
    """Schema for updating an issue"""
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[Annotated[str, BeforeValidator(clean_markdown)]] = Field(None, min_length=10)
    severity: Optional[IssueSeverity] = None
    status: Optional[IssueStatus] = None
    assignee_id: Optional[int] = None
    
    @model_validator(mode='after')
    def check_at_least_one_field(self) -> 'IssueUpdate':
        """Validate that at least one field is provided for update"""
        if all(v is None for v in [self.title, self.description, self.severity, self.status, self.assignee_id]):
            raise ValueError('At least one field must be provided for update')
        return self
    
    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate that title is not empty or just whitespace if provided"""
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip() if v is not None else v

class IssueInDB(IssueBase):
    """Schema for issue data from database"""
    id: int
    reporter_id: int
    assignee_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

class IssueWithRelations(IssueInDB):
    """Schema for issue with related data"""
    reporter: dict  # Simplified user info
    assignee: Optional[dict] = None  # Simplified user info
    tags: List[dict] = []  # List of tags
    attachment_count: int = 0
    comment_count: int = 0

class IssueResponse(BaseAPIResponse):
    """API response with issue data"""
    data: IssueWithRelations

class IssuesResponse(BaseAPIResponse):
    """API response with multiple issues"""
    data: List[IssueWithRelations]
    total: int
    page: int
    page_size: int

class IssueStatusUpdate(BaseSchema):
    """Schema for updating issue status"""
    status: IssueStatus
    comment: Optional[str] = None

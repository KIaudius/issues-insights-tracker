from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.user import UserRole
from app.schemas.base import BaseSchema, BaseAPIResponse

class UserBase(BaseSchema):
    """Base schema for user data"""
    email: EmailStr
    name: str
    role: UserRole = UserRole.REPORTER
    is_active: bool = True

class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str = Field(..., min_length=8)
    
    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        return v

class UserUpdate(BaseSchema):
    """Schema for updating a user"""
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)
    
    @field_validator('password')
    @classmethod
    def password_strength(cls, v: Optional[str]) -> Optional[str]:
        """Validate password strength if provided"""
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        return v

class UserInDB(UserBase):
    """Schema for user data from database"""
    id: int
    created_at: str
    updated_at: str
    is_oauth_user: bool = False
    oauth_provider: Optional[str] = None
    profile_image: Optional[str] = None

class UserResponse(BaseAPIResponse):
    """API response with user data"""
    data: UserInDB

class UsersResponse(BaseAPIResponse):
    """API response with multiple users"""
    data: List[UserInDB]
    total: int
    page: int
    page_size: int

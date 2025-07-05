from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import BaseAPIResponse
from app.schemas.user import UserInDB

class Token(BaseModel):
    """Schema for JWT token"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    """Schema for JWT token payload"""
    sub: str  # User ID
    email: EmailStr
    role: str
    exp: int  # Expiration timestamp

class TokenResponse(BaseAPIResponse):
    """API response with token data"""
    data: Token
    user: UserInDB

class LoginRequest(BaseModel):
    """Schema for login request"""
    email: EmailStr
    password: str = Field(..., min_length=8)

class RefreshRequest(BaseModel):
    """Schema for token refresh request"""
    refresh_token: str

class PasswordResetRequest(BaseModel):
    """Schema for password reset request"""
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation"""
    token: str
    password: str = Field(..., min_length=8)

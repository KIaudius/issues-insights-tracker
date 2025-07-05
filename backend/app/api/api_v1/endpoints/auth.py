from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.crud.user import authenticate_user, get_user_by_email
from app.schemas.auth import TokenResponse, RefreshRequest
from app.schemas.user import UserCreate

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """OAuth2 compatible token login, get an access token for future requests"""
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access and refresh tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": str(user.id), "email": user.email, "role": user.role.value}
    
    return {
        "success": True,
        "data": {
            "access_token": create_access_token(token_data, expires_delta=access_token_expires),
            "refresh_token": create_refresh_token(token_data),
            "token_type": "bearer"
        },
        "user": user
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_request: RefreshRequest, db: Session = Depends(get_db)) -> Any:
    """Refresh access token"""
    try:
        from jose import jwt
        payload = jwt.decode(
            refresh_request.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        email = payload.get("email")
        if user_id is None or email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = get_user_by_email(db, email=email)
    if not user or str(user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create new access and refresh tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": str(user.id), "email": user.email, "role": user.role.value}
    
    return {
        "success": True,
        "data": {
            "access_token": create_access_token(token_data, expires_delta=access_token_expires),
            "refresh_token": create_refresh_token(token_data),
            "token_type": "bearer"
        },
        "user": user
    }

@router.post("/register", response_model=TokenResponse)
async def register_user(user_in: UserCreate, db: Session = Depends(get_db)) -> Any:
    """Register new user"""
    # Check if user with this email already exists
    user = get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create new user
    from app.crud.user import create_user
    user = create_user(db, user_in=user_in)
    
    # Create access and refresh tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": str(user.id), "email": user.email, "role": user.role.value}
    
    return {
        "success": True,
        "data": {
            "access_token": create_access_token(token_data, expires_delta=access_token_expires),
            "refresh_token": create_refresh_token(token_data),
            "token_type": "bearer"
        },
        "user": user
    }

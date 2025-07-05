from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_current_active_user, get_admin_user
from app.crud.user import get_user, get_users, create_user, update_user, delete_user
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UsersResponse

router = APIRouter()

@router.get("/", response_model=UsersResponse)
async def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    role: UserRole = None,
    current_user: User = Depends(get_admin_user)
) -> Any:
    """Retrieve users - admin only"""
    users = get_users(db, skip=skip, limit=limit, role=role)
    return {
        "success": True,
        "data": users,
        "total": len(users),
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit
    }

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user: User = Depends(get_admin_user)
) -> Any:
    """Create new user - admin only"""
    # Check if user with this email already exists
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    user = create_user(db, user_in=user_in)
    return {"success": True, "data": user}

@router.get("/me", response_model=UserResponse)
async def read_user_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Get current user"""
    return {"success": True, "data": current_user}

@router.put("/me", response_model=UserResponse)
async def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Update current user"""
    # Prevent users from changing their own role
    if user_in.role is not None and user_in.role != current_user.role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change own role"
        )
    
    user = update_user(db, db_user=current_user, user_in=user_in)
    return {"success": True, "data": user}

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
) -> Any:
    """Get user by ID - admin only"""
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"success": True, "data": user}

@router.put("/{user_id}", response_model=UserResponse)
async def update_user_endpoint(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(get_admin_user)
) -> Any:
    """Update user - admin only"""
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent changing own role
    if user.id == current_user.id and user_in.role is not None and user_in.role != current_user.role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change own role"
        )
    
    user = update_user(db, db_user=user, user_in=user_in)
    return {"success": True, "data": user}

@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user_endpoint(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: User = Depends(get_admin_user)
) -> Any:
    """Delete user - admin only"""
    user = get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent deleting self
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete own user account"
        )
    
    user = delete_user(db, user_id=user_id)
    return {"success": True, "data": user}

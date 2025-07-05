from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()

def get_users(
    db: Session, skip: int = 0, limit: int = 100, role: Optional[UserRole] = None
) -> List[User]:
    """Get users with optional role filter"""
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    return query.offset(skip).limit(limit).all()

def create_user(db: Session, user_in: UserCreate) -> User:
    """Create new user"""
    db_user = User(
        email=user_in.email,
        name=user_in.name,
        hashed_password=get_password_hash(user_in.password),
        role=user_in.role,
        is_active=user_in.is_active,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_oauth_user(db: Session, email: str, name: str, provider: str, profile_image: Optional[str] = None) -> User:
    """Create or update OAuth user"""
    db_user = get_user_by_email(db, email)
    if db_user:
        # Update existing user with OAuth info
        db_user.is_oauth_user = True
        db_user.oauth_provider = provider
        if profile_image:
            db_user.profile_image = profile_image
        db.commit()
        db.refresh(db_user)
        return db_user
    
    # Create new OAuth user
    db_user = User(
        email=email,
        name=name,
        hashed_password=None,  # OAuth users don't have passwords
        role=UserRole.REPORTER,  # Default role
        is_active=True,
        is_oauth_user=True,
        oauth_provider=provider,
        profile_image=profile_image
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: User, user_in: Union[UserUpdate, Dict[str, Any]]) -> User:
    """Update user"""
    if isinstance(user_in, dict):
        update_data = user_in
    else:
        update_data = user_in.model_dump(exclude_unset=True)
    
    # Handle password update
    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = get_password_hash(update_data["password"])
        del update_data["password"]
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> User:
    """Delete user"""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user with email and password"""
    user = get_user_by_email(db, email=email)
    if not user or user.is_oauth_user or not user.hashed_password:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

from typing import Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.core.security import get_current_active_user, get_admin_user, get_maintainer_or_admin_user
from app.models.user import User

def get_db() -> Generator[Session, None, None]:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

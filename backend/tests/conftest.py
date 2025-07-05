import os
import pytest
from typing import Dict, Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.database import Base, get_db
from app.main import app
from app.core.config import settings
from app.core.security import create_access_token
from app.models.user import UserRole

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db() -> Generator:
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new session for each test
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
    # Drop all tables after the test
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db) -> Generator:
    # Override the get_db dependency
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client
    with TestClient(app) as c:
        yield c
    
    # Reset dependency overrides
    app.dependency_overrides = {}

@pytest.fixture(scope="function")
def test_user(db) -> Dict:
    """Create a test user and return user data with tokens"""
    from app.models.user import User
    from app.core.security import get_password_hash
    
    # Create test user
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password"),
        full_name="Test User",
        role=UserRole.REPORTER,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create access token
    token_data = {"sub": str(user.id), "email": user.email, "role": user.role.value}
    access_token = create_access_token(token_data)
    
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "access_token": access_token,
        "token_type": "bearer"
    }

@pytest.fixture(scope="function")
def admin_user(db) -> Dict:
    """Create an admin user and return user data with tokens"""
    from app.models.user import User
    from app.core.security import get_password_hash
    
    # Create admin user
    user = User(
        email="admin@example.com",
        hashed_password=get_password_hash("password"),
        full_name="Admin User",
        role=UserRole.ADMIN,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create access token
    token_data = {"sub": str(user.id), "email": user.email, "role": user.role.value}
    access_token = create_access_token(token_data)
    
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "access_token": access_token,
        "token_type": "bearer"
    }

@pytest.fixture(scope="function")
def maintainer_user(db) -> Dict:
    """Create a maintainer user and return user data with tokens"""
    from app.models.user import User
    from app.core.security import get_password_hash
    
    # Create maintainer user
    user = User(
        email="maintainer@example.com",
        hashed_password=get_password_hash("password"),
        full_name="Maintainer User",
        role=UserRole.MAINTAINER,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create access token
    token_data = {"sub": str(user.id), "email": user.email, "role": user.role.value}
    access_token = create_access_token(token_data)
    
    return {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "access_token": access_token,
        "token_type": "bearer"
    }

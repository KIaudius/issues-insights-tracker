import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import UserRole

def test_read_users_admin(client, admin_user):
    """Test that admin can read all users"""
    response = client.get(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {admin_user['access_token']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)

def test_read_users_forbidden(client, test_user):
    """Test that non-admin cannot read all users"""
    response = client.get(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {test_user['access_token']}"}
    )
    assert response.status_code == 403

def test_read_user_me(client, test_user):
    """Test reading current user info"""
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {test_user['access_token']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == test_user["email"]

def test_update_user_me(client, test_user):
    """Test updating current user info"""
    response = client.put(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {test_user['access_token']}"},
        json={"full_name": "Updated Name"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["full_name"] == "Updated Name"

def test_update_user_me_role_forbidden(client, test_user):
    """Test that user cannot update their own role"""
    response = client.put(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {test_user['access_token']}"},
        json={"role": UserRole.ADMIN.value}
    )
    assert response.status_code == 400

def test_create_user_admin(client, admin_user):
    """Test that admin can create a new user"""
    response = client.post(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {admin_user['access_token']}"},
        json={
            "email": "newuser@example.com",
            "password": "password123",
            "full_name": "New User",
            "role": UserRole.REPORTER.value
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "newuser@example.com"
    assert data["data"]["role"] == UserRole.REPORTER.value

def test_create_user_forbidden(client, test_user):
    """Test that non-admin cannot create a new user"""
    response = client.post(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {test_user['access_token']}"},
        json={
            "email": "newuser@example.com",
            "password": "password123",
            "full_name": "New User",
            "role": UserRole.REPORTER.value
        }
    )
    assert response.status_code == 403

def test_delete_user_admin(client, admin_user, test_user, db: Session):
    """Test that admin can delete a user"""
    response = client.delete(
        f"/api/v1/users/{test_user['id']}",
        headers={"Authorization": f"Bearer {admin_user['access_token']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    # Verify user is deleted from database
    from app.models.user import User
    user = db.query(User).filter(User.id == test_user["id"]).first()
    assert user is None

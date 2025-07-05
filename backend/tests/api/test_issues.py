import pytest
import io
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.issue import IssueStatus, IssueSeverity

@pytest.fixture
def test_issue(client, test_user, db: Session):
    """Create a test issue"""
    response = client.post(
        "/api/v1/issues/",
        headers={"Authorization": f"Bearer {test_user['access_token']}"},
        data={
            "title": "Test Issue",
            "description": "This is a test issue",
            "severity": IssueSeverity.MEDIUM.value
        }
    )
    assert response.status_code == 201
    return response.json()["data"]

def test_create_issue(client, test_user):
    """Test creating a new issue"""
    response = client.post(
        "/api/v1/issues/",
        headers={"Authorization": f"Bearer {test_user['access_token']}"},
        data={
            "title": "New Issue",
            "description": "This is a new issue",
            "severity": IssueSeverity.HIGH.value
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "New Issue"
    assert data["data"]["severity"] == IssueSeverity.HIGH.value
    assert data["data"]["status"] == IssueStatus.OPEN.value
    assert data["data"]["reporter_id"] == test_user["id"]

def test_create_issue_with_file(client, test_user):
    """Test creating a new issue with file attachment"""
    # Create a test file
    file_content = b"test file content"
    file = io.BytesIO(file_content)
    
    response = client.post(
        "/api/v1/issues/",
        headers={"Authorization": f"Bearer {test_user['access_token']}"},
        data={
            "title": "Issue with File",
            "description": "This issue has a file attachment",
            "severity": IssueSeverity.MEDIUM.value
        },
        files={"file": ("test.txt", file, "text/plain")}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    
    # Check if issue was created with correct data
    assert data["data"]["title"] == "Issue with File"

def test_read_issues(client, test_user, test_issue):
    """Test reading issues list"""
    response = client.get(
        "/api/v1/issues/",
        headers={"Authorization": f"Bearer {test_user['access_token']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    assert data["total"] > 0

def test_read_issue(client, test_user, test_issue):
    """Test reading a specific issue"""
    response = client.get(
        f"/api/v1/issues/{test_issue['id']}",
        headers={"Authorization": f"Bearer {test_user['access_token']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["id"] == test_issue["id"]
    assert data["data"]["title"] == test_issue["title"]

def test_update_issue(client, test_user, test_issue):
    """Test updating an issue"""
    response = client.put(
        f"/api/v1/issues/{test_issue['id']}",
        headers={"Authorization": f"Bearer {test_user['access_token']}"},
        json={
            "title": "Updated Issue Title",
            "description": "Updated description"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "Updated Issue Title"
    assert data["data"]["description"] == "Updated description"

def test_reporter_cannot_change_status(client, test_user, test_issue):
    """Test that reporters cannot change issue status"""
    response = client.put(
        f"/api/v1/issues/{test_issue['id']}",
        headers={"Authorization": f"Bearer {test_user['access_token']}"},
        json={
            "status": IssueStatus.TRIAGED.value
        }
    )
    assert response.status_code == 403

def test_maintainer_can_change_status(client, maintainer_user, test_issue):
    """Test that maintainers can change issue status"""
    response = client.put(
        f"/api/v1/issues/{test_issue['id']}/status",
        headers={"Authorization": f"Bearer {maintainer_user['access_token']}"},
        json={
            "status": IssueStatus.TRIAGED.value,
            "comment": "Issue has been triaged"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == IssueStatus.TRIAGED.value

def test_admin_can_delete_issue(client, admin_user, test_issue):
    """Test that admin can delete an issue"""
    response = client.delete(
        f"/api/v1/issues/{test_issue['id']}",
        headers={"Authorization": f"Bearer {admin_user['access_token']}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    # Verify issue is deleted
    response = client.get(
        f"/api/v1/issues/{test_issue['id']}",
        headers={"Authorization": f"Bearer {admin_user['access_token']}"}
    )
    assert response.status_code == 404

def test_reporter_cannot_delete_issue(client, test_user, test_issue):
    """Test that reporters cannot delete issues"""
    response = client.delete(
        f"/api/v1/issues/{test_issue['id']}",
        headers={"Authorization": f"Bearer {test_user['access_token']}"}
    )
    assert response.status_code == 403

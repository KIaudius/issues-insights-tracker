from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status, Query, File, UploadFile, Form
from sqlalchemy.orm import Session
import json

from app.api.deps import get_db
from app.core.security import get_current_active_user, get_admin_user, get_maintainer_or_admin_user
from app.crud.issue import get_issue, get_issues, create_issue, update_issue, delete_issue, update_issue_status
from app.crud.attachment import save_upload_file, create_attachment
from app.models.user import User, UserRole
from app.models.issue import IssueStatus, IssueSeverity
from app.schemas.issue import IssueCreate, IssueUpdate, IssueResponse, IssuesResponse, IssueStatusUpdate
from app.schemas.attachment import AttachmentCreate

router = APIRouter()

@router.get("/", response_model=IssuesResponse)
async def read_issues(
    db: Session = Depends(get_db),
    skip: int = Query(0, description="Number of issues to skip (pagination offset)"),
    limit: int = Query(100, description="Maximum number of issues to return", ge=1, le=100),
    status: Optional[IssueStatus] = Query(None, description="Filter by status: OPEN, TRIAGED, IN_PROGRESS, DONE"),
    severity: Optional[IssueSeverity] = Query(None, description="Filter by severity: LOW, MEDIUM, HIGH, CRITICAL"),
    search: Optional[str] = Query(None, description="Search term for issue title or description"),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Retrieve a paginated list of issues based on filters.
    
    **Permission rules:**
    - Admins and maintainers can see all issues
    - Reporters can only see their own created issues
    
    **Pagination:**
    Use `skip` and `limit` parameters for pagination.
    The response includes total count and current page information.
    
    **Example:**
    ```
    GET /api/v1/issues/?status=OPEN&severity=HIGH&limit=10
    ```
    """
    issues, total = get_issues(
        db, 
        skip=skip, 
        limit=limit, 
        current_user=current_user,
        status=status,
        severity=severity,
        search=search
    )
    return {
        "success": True,
        "data": issues,
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit
    }

@router.post("/", response_model=IssueResponse, status_code=status.HTTP_201_CREATED)
async def create_issue_endpoint(
    *,
    db: Session = Depends(get_db),
    title: str = Form(..., description="Issue title, max 255 characters"),
    description: str = Form(..., description="Detailed issue description in Markdown format"),
    severity: IssueSeverity = Form(IssueSeverity.MEDIUM, description="Issue severity level"),
    assignee_id: Optional[int] = Form(None, description="Optional user ID to assign the issue to"),
    file: Optional[UploadFile] = File(None, description="Optional attachment file (max 10MB)"),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Create a new issue with optional file attachment.
    
    **Required fields:**
    - `title`: Issue title (max 255 characters)
    - `description`: Detailed description supporting Markdown formatting
    
    **Optional fields:**
    - `severity`: Issue priority level (LOW, MEDIUM, HIGH, CRITICAL)
    - `assignee_id`: User ID to assign the issue to (if known)
    - `file`: File attachment (supported formats: PDF, PNG, JPG, JPEG, GIF, DOC, DOCX, XLS, XLSX, TXT)
    
    **File restrictions:**
    - Maximum file size: 10MB
    - Supported extensions: .pdf, .png, .jpg, .jpeg, .gif, .doc, .docx, .xls, .xlsx, .txt
    
    The issue is automatically assigned to the current user as the reporter.
    The initial status is set to OPEN.
    
    **Example usage:**
    ```
    # Using form-data with curl:
    curl -X POST \
      "http://localhost:8000/api/v1/issues/" \
      -H "Authorization: Bearer {token}" \
      -F "title=New Issue" \
      -F "description=Description with **markdown**" \
      -F "severity=HIGH" \
      -F "file=@document.pdf"
    ```
    """
    # Create issue
    issue_in = IssueCreate(
        title=title,
        description=description,
        severity=severity,
        assignee_id=assignee_id
    )
    issue = create_issue(db, issue_in=issue_in, reporter_id=current_user.id)
    
    # Handle file upload if provided
    if file:
        try:
            file_path = await save_upload_file(file, issue.id)
            attachment_in = AttachmentCreate(
                filename=file.filename,
                content_type=file.content_type,
                size=file.size,
                issue_id=issue.id,
                file_path=file_path
            )
            create_attachment(db, attachment_in=attachment_in, uploader_id=current_user.id)
        except Exception as e:
            # Log the error but don't fail the issue creation
            print(f"Error uploading file: {str(e)}")
    
    # Refresh issue to get all relationships
    issue = get_issue(db, issue_id=issue.id)
    return {"success": True, "data": issue}

@router.get("/{issue_id}", response_model=IssueResponse)
async def read_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get issue by ID with RBAC"""
    issue = get_issue(db, issue_id=issue_id)
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.REPORTER and issue.reporter_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return {"success": True, "data": issue}

@router.put("/{issue_id}", response_model=IssueResponse)
async def update_issue_endpoint(
    *,
    db: Session = Depends(get_db),
    issue_id: int,
    issue_in: IssueUpdate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Update issue with RBAC"""
    issue = get_issue(db, issue_id=issue_id)
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.REPORTER:
        # Reporters can only update their own issues and cannot change status
        if issue.reporter_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        if issue_in.status is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Reporters cannot change issue status"
            )
    
    issue = update_issue(db, db_issue=issue, issue_in=issue_in, user_id=current_user.id)
    return {"success": True, "data": issue}

@router.put("/{issue_id}/status", response_model=IssueResponse)
async def update_issue_status_endpoint(
    *,
    db: Session = Depends(get_db),
    issue_id: int,
    status_update: IssueStatusUpdate,
    current_user: User = Depends(get_maintainer_or_admin_user)  # Only maintainers and admins
) -> Any:
    """Update issue status - maintainers and admins only"""
    issue = get_issue(db, issue_id=issue_id)
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    try:
        issue = update_issue_status(db, db_issue=issue, status_update=status_update, user_id=current_user.id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return {"success": True, "data": issue}

@router.delete("/{issue_id}", response_model=IssueResponse)
async def delete_issue_endpoint(
    *,
    db: Session = Depends(get_db),
    issue_id: int,
    current_user: User = Depends(get_admin_user)  # Admin only
) -> Any:
    """Delete issue - admin only"""
    issue = get_issue(db, issue_id=issue_id)
    if not issue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Issue not found"
        )
    
    issue = delete_issue(db, issue_id=issue_id)
    return {"success": True, "data": issue}

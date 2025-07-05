from typing import Any, Dict, Optional, Union, List, Tuple
from datetime import datetime

from sqlalchemy import func, or_, and_
from sqlalchemy.orm import Session, joinedload

from app.models.issue import Issue, IssueStatus, IssueSeverity
from app.models.user import User, UserRole
from app.models.issue_history import IssueHistory
from app.schemas.issue import IssueCreate, IssueUpdate, IssueStatusUpdate

def get_issue(db: Session, issue_id: int) -> Optional[Issue]:
    """Get issue by ID with related data"""
    return db.query(Issue).options(
        joinedload(Issue.reporter),
        joinedload(Issue.assignee),
        joinedload(Issue.tags),
    ).filter(Issue.id == issue_id).first()

def get_issues(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    current_user: Optional[User] = None,
    status: Optional[IssueStatus] = None,
    severity: Optional[IssueSeverity] = None,
    search: Optional[str] = None
) -> Tuple[List[Issue], int]:
    """Get issues with filters and RBAC"""
    query = db.query(Issue).options(
        joinedload(Issue.reporter),
        joinedload(Issue.assignee),
        joinedload(Issue.tags),
    )
    
    # Apply role-based access control
    if current_user:
        if current_user.role == UserRole.REPORTER:
            # Reporters can only see their own issues
            query = query.filter(Issue.reporter_id == current_user.id)
    
    # Apply filters
    if status:
        query = query.filter(Issue.status == status)
    if severity:
        query = query.filter(Issue.severity == severity)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Issue.title.ilike(search_term),
                Issue.description.ilike(search_term)
            )
        )
    
    # Get total count for pagination
    total = query.count()
    
    # Apply pagination
    issues = query.order_by(Issue.created_at.desc()).offset(skip).limit(limit).all()
    
    return issues, total

def create_issue(db: Session, issue_in: IssueCreate, reporter_id: int) -> Issue:
    """Create new issue"""
    db_issue = Issue(
        title=issue_in.title,
        description=issue_in.description,
        severity=issue_in.severity,
        status=IssueStatus.OPEN,  # Always start with OPEN
        reporter_id=reporter_id,
        assignee_id=issue_in.assignee_id
    )
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    
    # Create initial history entry
    history_entry = IssueHistory(
        issue_id=db_issue.id,
        user_id=reporter_id,
        old_status=None,  # Initial creation
        new_status=IssueStatus.OPEN,
        comment="Issue created"
    )
    db.add(history_entry)
    db.commit()
    
    return db_issue

def update_issue(db: Session, db_issue: Issue, issue_in: Union[IssueUpdate, Dict[str, Any]], user_id: int) -> Issue:
    """Update issue"""
    if isinstance(issue_in, dict):
        update_data = issue_in
    else:
        update_data = issue_in.model_dump(exclude_unset=True)
    
    # Track status change for history
    old_status = db_issue.status
    new_status = update_data.get("status")
    
    # Update issue fields
    for field, value in update_data.items():
        setattr(db_issue, field, value)
    
    db.commit()
    db.refresh(db_issue)
    
    # Create history entry if status changed
    if new_status and old_status != new_status:
        history_entry = IssueHistory(
            issue_id=db_issue.id,
            user_id=user_id,
            old_status=old_status,
            new_status=new_status,
            comment=f"Status changed from {old_status} to {new_status}"
        )
        db.add(history_entry)
        db.commit()
    
    return db_issue

def update_issue_status(db: Session, db_issue: Issue, status_update: IssueStatusUpdate, user_id: int) -> Issue:
    """Update issue status with validation"""
    if not db_issue.can_transition_to(status_update.status):
        raise ValueError(f"Cannot transition from {db_issue.status} to {status_update.status}")
    
    old_status = db_issue.status
    db_issue.status = status_update.status
    db.commit()
    db.refresh(db_issue)
    
    # Create history entry
    history_entry = IssueHistory(
        issue_id=db_issue.id,
        user_id=user_id,
        old_status=old_status,
        new_status=status_update.status,
        comment=status_update.comment
    )
    db.add(history_entry)
    db.commit()
    
    return db_issue

def delete_issue(db: Session, issue_id: int) -> Issue:
    """Delete issue"""
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if issue:
        db.delete(issue)
        db.commit()
    return issue

def get_issue_counts_by_status(db: Session) -> Dict[str, int]:
    """Get issue counts grouped by status"""
    results = db.query(
        Issue.status,
        func.count(Issue.id).label("count")
    ).group_by(Issue.status).all()
    
    return {status.value: count for status, count in results}

def get_issue_counts_by_severity(db: Session) -> Dict[str, int]:
    """Get issue counts grouped by severity"""
    results = db.query(
        Issue.severity,
        func.count(Issue.id).label("count")
    ).group_by(Issue.severity).all()
    
    return {severity.value: count for severity, count in results}

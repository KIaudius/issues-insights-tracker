from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_current_active_user, get_admin_user
from app.crud.comment_crud import get_comment, get_comments_by_issue, create_comment, update_comment, delete_comment, can_modify_comment
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse, CommentsResponse

router = APIRouter()

@router.get("/issue/{issue_id}", response_model=CommentsResponse)
async def read_comments_by_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Retrieve comments for an issue"""
    comments, total = get_comments_by_issue(
        db, 
        issue_id=issue_id,
        skip=skip, 
        limit=limit,
        current_user=current_user
    )
    return {
        "success": True,
        "data": comments,
        "total": total,
        "page": skip // limit + 1 if limit > 0 else 1,
        "page_size": limit
    }

@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment_endpoint(
    *,
    db: Session = Depends(get_db),
    comment_in: CommentCreate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Create new comment"""
    comment = create_comment(db, comment_in=comment_in, user_id=current_user.id)
    return {"success": True, "data": comment}

@router.get("/{comment_id}", response_model=CommentResponse)
async def read_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get comment by ID"""
    comment = get_comment(db, comment_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    return {"success": True, "data": comment}

@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment_endpoint(
    *,
    db: Session = Depends(get_db),
    comment_id: int,
    comment_in: CommentUpdate,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Update comment with permission check"""
    comment = get_comment(db, comment_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Check permissions
    if not can_modify_comment(comment, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    comment = update_comment(db, db_comment=comment, comment_in=comment_in)
    return {"success": True, "data": comment}

@router.delete("/{comment_id}", response_model=CommentResponse)
async def delete_comment_endpoint(
    *,
    db: Session = Depends(get_db),
    comment_id: int,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Delete comment with permission check"""
    comment = get_comment(db, comment_id=comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    # Check permissions
    if not can_modify_comment(comment, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    comment = delete_comment(db, comment_id=comment_id)
    return {"success": True, "data": comment}

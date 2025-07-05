from typing import List, Optional, Tuple

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from app.models.comment import Comment
from app.models.user import User, UserRole
from app.schemas.comment import CommentCreate, CommentUpdate

def get_comment(db: Session, comment_id: int) -> Optional[Comment]:
    """Get comment by ID with user data"""
    return db.query(Comment).options(joinedload(Comment.user)).filter(Comment.id == comment_id).first()

def get_comments_by_issue(
    db: Session, 
    issue_id: int, 
    skip: int = 0, 
    limit: int = 100,
    current_user: Optional[User] = None
) -> Tuple[List[Comment], int]:
    """Get comments for an issue with pagination"""
    query = db.query(Comment).options(joinedload(Comment.user)).filter(Comment.issue_id == issue_id)
    
    # Get total count for pagination
    total = query.count()
    
    # Apply pagination
    comments = query.order_by(Comment.created_at.asc()).offset(skip).limit(limit).all()
    
    return comments, total

def create_comment(db: Session, comment_in: CommentCreate, user_id: int) -> Comment:
    """Create new comment"""
    db_comment = Comment(
        content=comment_in.content,
        issue_id=comment_in.issue_id,
        user_id=user_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def update_comment(db: Session, db_comment: Comment, comment_in: CommentUpdate) -> Comment:
    """Update comment"""
    update_data = comment_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_comment, field, value)
    
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int) -> Comment:
    """Delete comment"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment

def can_modify_comment(comment: Comment, user: User) -> bool:
    """Check if user can modify or delete comment"""
    # Admin can modify any comment
    if user.role == UserRole.ADMIN:
        return True
    
    # Users can modify their own comments
    return comment.user_id == user.id

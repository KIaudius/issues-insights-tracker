from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.issue import IssueStatus

class IssueHistory(BaseModel):
    """Issue history model to track status changes"""
    old_status = Column(Enum(IssueStatus), nullable=True)  # Null for initial creation
    new_status = Column(Enum(IssueStatus), nullable=False)
    comment = Column(Text, nullable=True)  # Optional comment about the change
    
    # Foreign keys
    issue_id = Column(Integer, ForeignKey("issue.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)  # User who made the change
    
    # Relationships
    issue = relationship("Issue", back_populates="history")
    user = relationship("User")

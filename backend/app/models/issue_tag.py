from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class IssueTag(BaseModel):
    """Issue tag model for categorizing issues"""
    name = Column(String(50), nullable=False)
    color = Column(String(7), nullable=False, default="#3498db")  # Hex color code
    
    # Foreign keys
    issue_id = Column(Integer, ForeignKey("issue.id"), nullable=False)
    
    # Relationships
    issue = relationship("Issue", back_populates="tags")

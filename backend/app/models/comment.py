from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Comment(BaseModel):
    """Comment model for issues"""
    content = Column(Text, nullable=False)  # Can contain markdown
    
    # Foreign keys
    issue_id = Column(Integer, ForeignKey("issue.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    
    # Relationships
    issue = relationship("Issue", back_populates="comments")
    user = relationship("User", back_populates="comments")

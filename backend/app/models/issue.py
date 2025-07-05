from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from app.models.base import BaseModel

class IssueSeverity(str, PyEnum):
    """Enum for issue severity levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class IssueStatus(str, PyEnum):
    """Enum for issue status in workflow"""
    OPEN = "OPEN"  # Initial state
    TRIAGED = "TRIAGED"  # Reviewed and prioritized
    IN_PROGRESS = "IN_PROGRESS"  # Being worked on
    DONE = "DONE"  # Completed

class Issue(BaseModel):
    """Issue model with workflow states"""
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)  # Markdown content
    severity = Column(Enum(IssueSeverity), default=IssueSeverity.MEDIUM, nullable=False)
    status = Column(Enum(IssueStatus), default=IssueStatus.OPEN, nullable=False)
    
    # Foreign keys
    reporter_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("user.id"), nullable=True)  # Optional assignee
    
    # Relationships
    reporter = relationship("User", back_populates="reported_issues", foreign_keys=[reporter_id])
    assignee = relationship("User", back_populates="assigned_issues", foreign_keys=[assignee_id])
    comments = relationship("Comment", back_populates="issue", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="issue", cascade="all, delete-orphan")
    history = relationship("IssueHistory", back_populates="issue", cascade="all, delete-orphan")
    tags = relationship("IssueTag", back_populates="issue", cascade="all, delete-orphan")
    
    def can_transition_to(self, new_status: IssueStatus) -> bool:
        """Check if the issue can transition to the new status"""
        valid_transitions = {
            IssueStatus.OPEN: [IssueStatus.TRIAGED],
            IssueStatus.TRIAGED: [IssueStatus.IN_PROGRESS, IssueStatus.OPEN],
            IssueStatus.IN_PROGRESS: [IssueStatus.DONE, IssueStatus.TRIAGED],
            IssueStatus.DONE: [IssueStatus.IN_PROGRESS]
        }
        return new_status in valid_transitions.get(self.status, [])

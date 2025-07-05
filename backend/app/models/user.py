from sqlalchemy import Boolean, Column, Enum, String, Text
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from app.models.base import BaseModel

class UserRole(str, PyEnum):
    """Enum for user roles with increasing privileges"""
    REPORTER = "REPORTER"  # Can create and view own issues
    MAINTAINER = "MAINTAINER"  # Can triage any issue, add tags/status
    ADMIN = "ADMIN"  # Full CRUD on everything

class User(BaseModel):
    """User model with role-based access control"""
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=True)  # Nullable for OAuth users
    role = Column(Enum(UserRole), default=UserRole.REPORTER, nullable=False)
    is_active = Column(Boolean, default=True)
    is_oauth_user = Column(Boolean, default=False)
    oauth_provider = Column(String(50), nullable=True)  # e.g., 'google', 'github'
    profile_image = Column(String(255), nullable=True)
    
    # Relationships
    reported_issues = relationship("Issue", back_populates="reporter", foreign_keys="Issue.reporter_id")
    assigned_issues = relationship("Issue", back_populates="assignee", foreign_keys="Issue.assignee_id")
    comments = relationship("Comment", back_populates="user")
    
    def has_permission(self, min_role: UserRole) -> bool:
        """Check if user has at least the specified role level"""
        role_hierarchy = {
            UserRole.REPORTER: 1,
            UserRole.MAINTAINER: 2,
            UserRole.ADMIN: 3
        }
        return role_hierarchy.get(self.role, 0) >= role_hierarchy.get(min_role, 0)
    
    def is_admin(self) -> bool:
        """Check if user is an admin"""
        return self.role == UserRole.ADMIN
    
    def is_maintainer_or_above(self) -> bool:
        """Check if user is a maintainer or admin"""
        return self.role in [UserRole.MAINTAINER, UserRole.ADMIN]
    
    def is_reporter(self) -> bool:
        """Check if user is a reporter"""
        return self.role == UserRole.REPORTER

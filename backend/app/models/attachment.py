from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class Attachment(BaseModel):
    """Attachment model for issue file uploads"""
    filename = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)  # Path to file on disk or S3 key
    content_type = Column(String(100), nullable=False)  # MIME type
    size = Column(Integer, nullable=False)  # File size in bytes
    
    # Foreign keys
    issue_id = Column(Integer, ForeignKey("issue.id"), nullable=False)
    uploader_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    
    # Relationships
    issue = relationship("Issue", back_populates="attachments")
    uploader = relationship("User")
    
    @property
    def is_image(self) -> bool:
        """Check if the attachment is an image"""
        return self.content_type.startswith('image/')
    
    @property
    def is_pdf(self) -> bool:
        """Check if the attachment is a PDF"""
        return self.content_type == 'application/pdf'
    
    @property
    def is_previewable(self) -> bool:
        """Check if the attachment can be previewed in browser"""
        return self.is_image or self.is_pdf

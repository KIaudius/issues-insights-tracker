from sqlalchemy import Column, Date, Integer, String

from app.models.base import BaseModel

class DailyStats(BaseModel):
    """Daily statistics model for background job aggregation"""
    date = Column(Date, nullable=False, index=True, unique=True)
    
    # Issue counts by status
    open_count = Column(Integer, default=0, nullable=False)
    triaged_count = Column(Integer, default=0, nullable=False)
    in_progress_count = Column(Integer, default=0, nullable=False)
    done_count = Column(Integer, default=0, nullable=False)
    
    # Issue counts by severity
    low_severity_count = Column(Integer, default=0, nullable=False)
    medium_severity_count = Column(Integer, default=0, nullable=False)
    high_severity_count = Column(Integer, default=0, nullable=False)
    critical_severity_count = Column(Integer, default=0, nullable=False)
    
    # Other metrics
    total_issues = Column(Integer, default=0, nullable=False)
    new_issues = Column(Integer, default=0, nullable=False)
    closed_issues = Column(Integer, default=0, nullable=False)
    avg_resolution_time = Column(Integer, default=0, nullable=False)  # In hours

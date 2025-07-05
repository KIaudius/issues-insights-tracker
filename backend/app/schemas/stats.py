from typing import List, Dict, Any
from datetime import date
from pydantic import Field

from app.schemas.base import BaseSchema, BaseAPIResponse

class DailyStatsBase(BaseSchema):
    """Base schema for daily statistics"""
    date: date
    open_count: int = 0
    triaged_count: int = 0
    in_progress_count: int = 0
    done_count: int = 0
    low_severity_count: int = 0
    medium_severity_count: int = 0
    high_severity_count: int = 0
    critical_severity_count: int = 0
    total_issues: int = 0
    new_issues: int = 0
    closed_issues: int = 0
    avg_resolution_time: int = 0  # In hours

class DailyStatsInDB(DailyStatsBase):
    """Schema for daily statistics from database"""
    id: int

class DailyStatsResponse(BaseAPIResponse):
    """API response with daily statistics"""
    data: DailyStatsInDB

class DailyStatsListResponse(BaseAPIResponse):
    """API response with multiple daily statistics"""
    data: List[DailyStatsInDB]

class DashboardStats(BaseSchema):
    """Schema for dashboard statistics"""
    issue_counts_by_status: Dict[str, int]
    issue_counts_by_severity: Dict[str, int]
    recent_activity: List[Dict[str, Any]]
    resolution_times: Dict[str, float]  # Average resolution time by severity

class DashboardResponse(BaseAPIResponse):
    """API response with dashboard data"""
    data: DashboardStats

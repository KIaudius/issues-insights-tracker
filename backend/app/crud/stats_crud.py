from typing import List, Dict, Any, Optional
from datetime import date, datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.daily_stats import DailyStats
from app.models.issue import Issue, IssueStatus, IssueSeverity
from app.models.issue_history import IssueHistory

def get_daily_stats(db: Session, stats_date: date) -> Optional[DailyStats]:
    """Get daily statistics for a specific date"""
    return db.query(DailyStats).filter(DailyStats.date == stats_date).first()

def get_daily_stats_range(db: Session, start_date: date, end_date: date) -> List[DailyStats]:
    """Get daily statistics for a date range"""
    return db.query(DailyStats)\
        .filter(DailyStats.date >= start_date, DailyStats.date <= end_date)\
        .order_by(DailyStats.date.asc())\
        .all()

def create_or_update_daily_stats(db: Session, stats_date: date) -> DailyStats:
    """Create or update daily statistics for a specific date"""
    # Check if stats already exist for this date
    db_stats = get_daily_stats(db, stats_date)
    if not db_stats:
        # Create new stats
        db_stats = DailyStats(date=stats_date)
        db.add(db_stats)
    
    # Calculate issue counts by status
    status_counts = db.query(
        Issue.status,
        func.count(Issue.id)
    ).filter(
        func.date(Issue.created_at) <= stats_date
    ).group_by(Issue.status).all()
    
    # Update status counts
    for status, count in status_counts:
        if status == IssueStatus.OPEN:
            db_stats.open_count = count
        elif status == IssueStatus.TRIAGED:
            db_stats.triaged_count = count
        elif status == IssueStatus.IN_PROGRESS:
            db_stats.in_progress_count = count
        elif status == IssueStatus.DONE:
            db_stats.done_count = count
    
    # Calculate issue counts by severity
    severity_counts = db.query(
        Issue.severity,
        func.count(Issue.id)
    ).filter(
        func.date(Issue.created_at) <= stats_date
    ).group_by(Issue.severity).all()
    
    # Update severity counts
    for severity, count in severity_counts:
        if severity == IssueSeverity.LOW:
            db_stats.low_severity_count = count
        elif severity == IssueSeverity.MEDIUM:
            db_stats.medium_severity_count = count
        elif severity == IssueSeverity.HIGH:
            db_stats.high_severity_count = count
        elif severity == IssueSeverity.CRITICAL:
            db_stats.critical_severity_count = count
    
    # Calculate total issues
    db_stats.total_issues = db.query(func.count(Issue.id)).filter(
        func.date(Issue.created_at) <= stats_date
    ).scalar() or 0
    
    # Calculate new issues for this day
    db_stats.new_issues = db.query(func.count(Issue.id)).filter(
        func.date(Issue.created_at) == stats_date
    ).scalar() or 0
    
    # Calculate closed issues for this day
    db_stats.closed_issues = db.query(func.count(IssueHistory.id)).filter(
        func.date(IssueHistory.created_at) == stats_date,
        IssueHistory.new_status == IssueStatus.DONE
    ).scalar() or 0
    
    # Calculate average resolution time for issues closed on this day
    # This is more complex and would require joining with issue history
    # For simplicity, we'll use a placeholder calculation
    closed_issues = db.query(Issue).join(IssueHistory).filter(
        func.date(IssueHistory.created_at) == stats_date,
        IssueHistory.new_status == IssueStatus.DONE
    ).all()
    
    if closed_issues:
        total_hours = 0
        for issue in closed_issues:
            # Calculate time from creation to closing
            # In a real app, we'd use the actual timestamps from history
            resolution_time = (issue.updated_at - issue.created_at).total_seconds() / 3600
            total_hours += resolution_time
        
        db_stats.avg_resolution_time = int(total_hours / len(closed_issues))
    
    db.commit()
    db.refresh(db_stats)
    return db_stats

def get_dashboard_stats(db: Session) -> Dict[str, Any]:
    """Get statistics for dashboard"""
    # Get issue counts by status
    status_counts = db.query(
        Issue.status,
        func.count(Issue.id)
    ).group_by(Issue.status).all()
    
    issue_counts_by_status = {status.value: count for status, count in status_counts}
    
    # Get issue counts by severity
    severity_counts = db.query(
        Issue.severity,
        func.count(Issue.id)
    ).group_by(Issue.severity).all()
    
    issue_counts_by_severity = {severity.value: count for severity, count in severity_counts}
    
    # Get recent activity (last 10 status changes)
    recent_activity = db.query(IssueHistory)\
        .order_by(IssueHistory.created_at.desc())\
        .limit(10)\
        .all()
    
    recent_activity_data = [
        {
            "id": activity.id,
            "issue_id": activity.issue_id,
            "user_id": activity.user_id,
            "old_status": activity.old_status.value if activity.old_status else None,
            "new_status": activity.new_status.value,
            "created_at": activity.created_at.isoformat(),
            "comment": activity.comment
        }
        for activity in recent_activity
    ]
    
    # Calculate average resolution times by severity
    # This would be more complex in a real app
    # For now, we'll use placeholder data
    resolution_times = {
        "LOW": 48.0,  # hours
        "MEDIUM": 36.0,
        "HIGH": 24.0,
        "CRITICAL": 12.0
    }
    
    return {
        "issue_counts_by_status": issue_counts_by_status,
        "issue_counts_by_severity": issue_counts_by_severity,
        "recent_activity": recent_activity_data,
        "resolution_times": resolution_times
    }

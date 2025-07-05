from typing import Any, List
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import get_current_active_user, get_maintainer_or_admin_user
from app.crud.stats_crud import get_daily_stats, get_daily_stats_range, create_or_update_daily_stats, get_dashboard_stats
from app.models.user import User
from app.schemas.stats import DailyStatsResponse, DailyStatsListResponse, DashboardStatsResponse

router = APIRouter()

@router.get("/dashboard", response_model=DashboardStatsResponse)
async def read_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get statistics for dashboard"""
    stats = get_dashboard_stats(db)
    return {"success": True, "data": stats}

@router.get("/daily", response_model=DailyStatsResponse)
async def read_daily_stats_endpoint(
    stats_date: date = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_maintainer_or_admin_user)  # Only maintainers and admins
) -> Any:
    """Get daily statistics for a specific date"""
    if stats_date is None:
        stats_date = date.today()
    
    stats = get_daily_stats(db, stats_date=stats_date)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Statistics not found for this date"
        )
    
    return {"success": True, "data": stats}

@router.get("/daily/range", response_model=DailyStatsListResponse)
async def read_daily_stats_range_endpoint(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_maintainer_or_admin_user)  # Only maintainers and admins
) -> Any:
    """Get daily statistics for a date range"""
    # Validate date range
    if end_date < start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date"
        )
    
    # Limit range to 90 days to prevent excessive queries
    if (end_date - start_date).days > 90:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Date range cannot exceed 90 days"
        )
    
    stats = get_daily_stats_range(db, start_date=start_date, end_date=end_date)
    return {
        "success": True,
        "data": stats,
        "total": len(stats)
    }

@router.post("/daily/generate", response_model=DailyStatsResponse)
async def generate_daily_stats_endpoint(
    stats_date: date = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_maintainer_or_admin_user)  # Only maintainers and admins
) -> Any:
    """Generate or update daily statistics for a specific date"""
    if stats_date is None:
        stats_date = date.today()
    
    # Don't allow generating stats for future dates
    if stats_date > date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot generate statistics for future dates"
        )
    
    stats = create_or_update_daily_stats(db, stats_date=stats_date)
    return {"success": True, "data": stats}

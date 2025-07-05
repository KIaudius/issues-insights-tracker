import logging
from datetime import datetime, date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.crud.stats import create_or_update_daily_stats

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_daily_stats():
    """Generate daily statistics for yesterday"""
    yesterday = date.today() - timedelta(days=1)
    logger.info(f"Generating daily statistics for {yesterday}")
    
    db = SessionLocal()
    try:
        stats = create_or_update_daily_stats(db, stats_date=yesterday)
        logger.info(f"Daily statistics generated successfully for {yesterday}")
        return stats
    except Exception as e:
        logger.error(f"Error generating daily statistics: {str(e)}")
        raise
    finally:
        db.close()

def job_execution_listener(event):
    """Monitor job execution and log status"""
    if event.code == EVENT_JOB_EXECUTED:
        logger.info(f"Job {event.job_id} executed successfully at {datetime.now()}")
    elif event.code == EVENT_JOB_ERROR:
        logger.error(f"Job {event.job_id} failed with exception: {event.exception}")
        # In a real production system, you might want to send an alert here
        # Example: notify_job_failure(event.job_id, str(event.exception))

def init_scheduler():
    """Initialize the background scheduler"""
    scheduler = BackgroundScheduler()
    
    # Schedule stats aggregation every 30 minutes as per requirements
    scheduler.add_job(
        generate_daily_stats,
        IntervalTrigger(minutes=30),
        id="stats_aggregation_job",
        replace_existing=True,
        max_instances=1,  # Prevent overlapping executions
        coalesce=True,    # Only run once if multiple executions are missed
        misfire_grace_time=300  # Allow 5-minute grace period for misfires
    )
    
    # Add job execution listener for monitoring
    scheduler.add_listener(
        job_execution_listener,
        EVENT_JOB_EXECUTED | EVENT_JOB_ERROR
    )
    
    # Start the scheduler
    scheduler.start()
    logger.info("Background scheduler started with 30-minute intervals")
    
    return scheduler

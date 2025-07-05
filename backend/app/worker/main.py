import logging
import time
from app.worker.scheduler import init_scheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Main worker entry point"""
    logger.info("Starting background worker")
    
    # Initialize the scheduler
    scheduler = init_scheduler()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down background worker")
        scheduler.shutdown()

if __name__ == "__main__":
    main()

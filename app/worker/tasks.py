from celery import shared_task
from checker import WebsiteCheker
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def check_website(self, url: str, timeout: int = 10) -> dict:
    """Website checking task"""
    try:
        result = WebsiteCheker.comprehensive_check(url, timeout)

        logger.info(f"Check completed for {url}")
        logger.info(f"Availability: {result['availability']}")
        if result.get('ssl'):
            logger.info(f"SSL: {result['ssl']}")
        
        if not result['availability']['available']:
            logger.warning(f"Website {url} is unavailable!")
        
        if result.get('ssl') and result['ssl'].get('is_warning'):
            logger.warning(f"SSL certificate for {url} expires in {result['ssl']['days_remaining']} days!")
        
        return result
        
    except Exception as e:
        logger.error(f"Error checking {url}: {str(e)}")
        self.retry(exc=e, countdown=30)
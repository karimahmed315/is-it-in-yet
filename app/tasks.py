# is-it-in-yet/app/tasks.py

from .extensions import celery
from urllib.parse import urlparse
import logging

@celery.task
def run_scrape_task(alert_id: int):
    """
    The background task that performs the scraping for a given alert.
    """
    # We import these here to avoid circular dependencies
    from app import create_app, db
    from app.models import Alert
    from app.services.scraper import scrape_product_data

    flask_app = create_app()
    with flask_app.app_context():
        try:
            alert = Alert.query.get(alert_id)
            if not alert:
                logging.warning(f"Alert with ID {alert_id} not found.")
                return

            logging.info(f"Running scrape task for Alert ID: {alert_id}")
            scraped_data = scrape_product_data(alert.product_url)

            alert.status = scraped_data['status']
            alert.product_name = scraped_data.get('name', alert.product_name)
            alert.product_image_url = scraped_data.get('image_url', alert.product_image_url)
            alert.product_price = scraped_data.get('price', alert.product_price)
            alert.website_domain = urlparse(alert.product_url).netloc.replace('www.', '')
            
            db.session.commit()
            logging.info(f"Successfully updated Alert ID: {alert_id}")

        except Exception as e:
            logging.error(f"Error in scrape task for Alert ID {alert_id}: {e}", exc_info=True)

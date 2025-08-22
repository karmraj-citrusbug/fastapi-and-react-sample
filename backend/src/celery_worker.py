from celery import Celery
from celery.schedules import schedule

from config.settings import app_settings

REDIS_BROKER = app_settings.REDIS_BROKER_URL

celery_app = Celery("worker", broker=REDIS_BROKER, backend=REDIS_BROKER)
celery_app.conf.timezone = "UTC"

# Register with beat dynamically
celery_app.conf.beat_schedule = {
    "alpha-vantage-events-data-every-N-seconds": {
        "task": "src.infrastructure.tasks.process_alpha_vantage_events_data",
        "schedule": schedule(run_every=60 * 15),  # Run every 15 minutes
    },
    "news-events-data-every-N-seconds": {
        "task": "src.infrastructure.tasks.process_news_events_data",
        "schedule": schedule(run_every=60 * 60 * 24),  # Run once a day
    },
}

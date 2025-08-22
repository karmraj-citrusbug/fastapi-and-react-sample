import asyncio
import logging

from celery import group

from src.celery_worker import celery_app
from src.domain.enums import MarketEventSource
from src.infrastructure.news_fetcher.core.alpha_vantage_news_fetcher import (
    AlphaVantageNewsFetcher,
)
from src.infrastructure.news_fetcher.core.event_registry_news_fetcher import (
    EventRegistryNewsFetcher,
)
from src.infrastructure.news_fetcher.orchestrator import process_article_task

logger = logging.getLogger(__name__)


@celery_app.task
def process_alpha_vantage_events_data() -> None:
    logger.info("Processing alpha vantage news events")
    try:
        source = MarketEventSource.ALPHA_VANTAGE_API
        events_fetcher = AlphaVantageNewsFetcher()
        # Create an event loop and run the async function
        events = asyncio.run(events_fetcher.fetch_news())

        # Process articles in parallel using Celery
        job = group(process_article_task.s(article, source) for article in events)
        job.apply_async()

    except Exception as e:
        logger.error(f"Error processing Alpha Vantage events: {e}", exc_info=True)


@celery_app.task
def process_news_events_data() -> None:
    logger.info("Processing news events")
    try:
        source = MarketEventSource.EVENT_REGISTRY_API
        events_fetcher = EventRegistryNewsFetcher()
        # Create an event loop and run the async function
        events = asyncio.run(events_fetcher.fetch_news())

        # Process articles in parallel using Celery
        job = group(process_article_task.s(article, source) for article in events)
        job.apply_async()

    except Exception as e:
        logger.error(f"Error processing news events: {e}", exc_info=True)


@celery_app.task
def process_customized_news_events_data(event_title: str, user_id: str) -> None:
    logger.info("Processing customized news events")
    try:
        # Create an event loop for async operations
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        source = MarketEventSource.CUSTOM_EVENT

        article = {
            "title": event_title,
            "summary": "",
            "banner_image": "",
        }

        async def process_custom_event():
            process_article_task.delay(article, source, user_id)

        try:
            # Run the async function in the event loop
            loop.run_until_complete(process_custom_event())
        finally:
            # Always clean up the loop
            loop.close()

    except Exception as e:
        logger.error(f"Error processing news events: {e}", exc_info=True)

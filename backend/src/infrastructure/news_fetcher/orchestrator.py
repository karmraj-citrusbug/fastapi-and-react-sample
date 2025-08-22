import asyncio
import logging
from typing import Any, Dict, Optional

from src.celery_worker import celery_app
from src.domain.enums import MarketEvenProcessingtStatus, MarketEventSource, PostStatus
from src.domain.market_events.services import (
    MarketEventDataClass,
    MarketEventDomainServices,
    MarketEventFactory,
)
from src.domain.posts.services import PostDataClass, PostDomainServices, PostFactory
from src.infrastructure.news_fetcher.news_pipeline import NewsPipeline
from src.infrastructure.utils import get_current_timestamp_with_timezone
from src.infrastructure.websockets.redis_listener import publish_updates
from src.schema.market_events import RunTimeMarketEventSchema, UpdateMarketEventSchema
from src.schema.utils import WebsocketMessageTypesEnum

logger = logging.getLogger(__name__)

pipeline = NewsPipeline()
market_event_domain_services = MarketEventDomainServices()
post_domain_services = PostDomainServices()


@celery_app.task
def process_article_task(
    article: Dict[str, Any],
    source: MarketEventSource,
    user_id: Optional[str] = None,
) -> None:
    try:
        if not user_id:
            classification = pipeline.classify_financial_article(article)

            if not classification.get("is_financial"):
                logger.info(f"Article skipped: {article.get('title')}")
                return

        market_event_dataclass = MarketEventDataClass(
            title=article["title"],
            description=article["summary"],
            processing_status=MarketEvenProcessingtStatus.RESEARCHING,
            source=source,
            is_customized=True if user_id else False,
        )
        market_event_data = MarketEventFactory.build_entity_with_id(
            data=market_event_dataclass
        )
        market_event_domain_services.create_market_event(
            market_event_data=market_event_data
        )

        runtime_market_event_dto = RunTimeMarketEventSchema(
            id=str(market_event_data.id),
            title=market_event_dataclass.title,
            banner=None,
            sentimental_analysis=None,
            priority_flag=None,
            compliance_check=None,
            description=market_event_dataclass.description,
            deep_research_content=None,
            ai_generated_summarized_content=None,
            processing_status=market_event_dataclass.processing_status,
            source=market_event_dataclass.source,
            editable=False,
            updated_at=get_current_timestamp_with_timezone(),
        )

        broadcast_market_event_update_task.delay(
            runtime_market_event_dto.model_dump(),
            article,
            user_id,
        )

    except Exception as e:
        logger.error(
            f"Error processing article: {e}:{e.__traceback__.tb_lineno}", exc_info=True
        )


@celery_app.task
def broadcast_market_event_update_task(
    runtime_market_event_dto_dict: dict,
    article: dict,
    user_id: Optional[str] = None,
):
    try:
        runtime_market_event_dto = RunTimeMarketEventSchema(
            **runtime_market_event_dto_dict
        )

        # Create an event loop for async operations
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def process_updates():
            try:
                # Generate AI processing title
                runtime_market_event_dto.banner = pipeline.generate_ai_processing_title(
                    article
                )
                runtime_market_event_dto.updated_at = (
                    get_current_timestamp_with_timezone()
                )
                await publish_updates(
                    user_id=user_id,
                    data_type=WebsocketMessageTypesEnum.USER_CUSTOM_EVENT
                    if user_id
                    else WebsocketMessageTypesEnum.LIVE_EVENTS,
                    data=runtime_market_event_dto.model_dump(),
                )

                # Deep research financial articles
                runtime_market_event_dto.deep_research_content = (
                    pipeline.deep_research_financial_article(article)
                )
                runtime_market_event_dto.processing_status = (
                    MarketEvenProcessingtStatus.WRITING
                )
                runtime_market_event_dto.updated_at = (
                    get_current_timestamp_with_timezone()
                )
                await publish_updates(
                    user_id=user_id,
                    data_type=WebsocketMessageTypesEnum.USER_CUSTOM_EVENT
                    if user_id
                    else WebsocketMessageTypesEnum.LIVE_EVENTS,
                    data=runtime_market_event_dto.model_dump(),
                )

                # Fetch summarized content
                runtime_market_event_dto.ai_generated_summarized_content = pipeline.fetch_summarized_content_from_deep_research(
                    deep_research_content=runtime_market_event_dto.deep_research_content
                    or "N/A",
                )
                runtime_market_event_dto.processing_status = (
                    MarketEvenProcessingtStatus.FETCHING_ANALYTICS
                )
                runtime_market_event_dto.updated_at = (
                    get_current_timestamp_with_timezone()
                )
                await publish_updates(
                    user_id=user_id,
                    data_type=WebsocketMessageTypesEnum.USER_CUSTOM_EVENT
                    if user_id
                    else WebsocketMessageTypesEnum.LIVE_EVENTS,
                    data=runtime_market_event_dto.model_dump(),
                )

                # Fetch sentimental analysis
                runtime_market_event_dto.sentimental_analysis = (
                    pipeline.fetch_sentimental_analysis(article)
                )
                runtime_market_event_dto.updated_at = (
                    get_current_timestamp_with_timezone()
                )
                await publish_updates(
                    user_id=user_id,
                    data_type=WebsocketMessageTypesEnum.USER_CUSTOM_EVENT
                    if user_id
                    else WebsocketMessageTypesEnum.LIVE_EVENTS,
                    data=runtime_market_event_dto.model_dump(),
                )

                # Fetch priority flag
                runtime_market_event_dto.priority_flag = pipeline.fetch_priority_flag(
                    article
                )
                runtime_market_event_dto.updated_at = (
                    get_current_timestamp_with_timezone()
                )
                await publish_updates(
                    user_id=user_id,
                    data_type=WebsocketMessageTypesEnum.USER_CUSTOM_EVENT
                    if user_id
                    else WebsocketMessageTypesEnum.LIVE_EVENTS,
                    data=runtime_market_event_dto.model_dump(),
                )

                # Fetch compliance check
                runtime_market_event_dto.compliance_check = (
                    pipeline.fetch_compliance_check(article)
                )
                runtime_market_event_dto.processing_status = (
                    MarketEvenProcessingtStatus.DRAFTED
                )
                runtime_market_event_dto.editable = True
                runtime_market_event_dto.updated_at = (
                    get_current_timestamp_with_timezone()
                )
                runtime_market_event_dto.banner = (
                    runtime_market_event_dto.banner.replace(
                        "AI processing:", ""
                    ).strip()
                )
                await publish_updates(
                    user_id=user_id,
                    data_type=WebsocketMessageTypesEnum.USER_CUSTOM_EVENT
                    if user_id
                    else WebsocketMessageTypesEnum.LIVE_EVENTS,
                    data=runtime_market_event_dto.model_dump(),
                )

                market_event_domain_services.update_market_event_by_id(
                    id=runtime_market_event_dto.id,
                    market_event_data=UpdateMarketEventSchema(
                        **runtime_market_event_dto.model_dump()
                    ),
                )

                if user_id:
                    post_dataclass = PostDataClass(
                        title=runtime_market_event_dto.title,
                        description=runtime_market_event_dto.deep_research_content,
                        user_id=user_id,
                        market_event_id=runtime_market_event_dto.id,
                        status=PostStatus.DRAFT,
                        is_customized=True if user_id else False,
                    )

                    post_data = PostFactory.build_entity_with_id(data=post_dataclass)
                    post_domain_services.create_post(post=post_data)
            except Exception as e:
                logger.error(
                    f"Error in async processing: {e}:{e.__traceback__.tb_lineno}",
                    exc_info=True,
                )
                raise

        try:
            # Run the async function in the event loop
            loop.run_until_complete(process_updates())
        finally:
            # Always clean up the loop
            loop.close()

    except Exception as e:
        logger.error(
            f"Error broadcasting article: {e}:{e.__traceback__.tb_lineno}",
            exc_info=True,
        )

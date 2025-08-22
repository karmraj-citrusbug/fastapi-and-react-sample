from dataclasses import asdict, dataclass
from uuid import uuid4

from sqlalchemy.orm import aliased
from sqlalchemy.sql import literal

from fastapi.responses import JSONResponse

from config.db_connection import db_service
from config.response_handler import ResponseHandler
from src.domain.enums import MarketEvenProcessingtStatus, MarketEventSource
from src.domain.market_events.models import MarketEvent
from src.domain.posts.models import Post
from src.schema.market_events import ListMarketEventDataModelSchema, MarketEventDataModelSchema, UpdateMarketEventSchema


@dataclass(frozen=True)
class MarketEventDataClass:
    """
    Data class for MarketEvent model.
    """

    title: str
    description: str
    processing_status: MarketEvenProcessingtStatus = (
        MarketEvenProcessingtStatus.RESEARCHING
    )
    source: MarketEventSource = MarketEventSource.EVENT_REGISTRY_API
    is_customized: bool = False


class MarketEventFactory:
    """
    MarketEventFactory class for MarketEvent model for creating runtime MarketEvent Objects
    """

    @staticmethod
    def build_entity_with_id(data: MarketEventDataClass) -> MarketEvent:
        """
        Method to create runtime MarketEvent object using dataclass.

        Args:
            data (MarketEventDataClass): A dataclass containing market event information.

        Returns:
            MarketEvent: A runtime MarketEvent object.
        """
        return MarketEvent(id=uuid4(), **asdict(data))


class MarketEventDomainServices:
    def __init__(self):
        """
        Constructor for MarketEventDomainServices class.
        """
        self.db_session = db_service.get_session()

    @staticmethod
    def get_market_event_factory():
        """
        Method to get MarketEventFactory object.

        Returns:
            MarketEventFactory: A MarketEventFactory object.
        """
        try:
            return MarketEventFactory
        except Exception as e:
            return ResponseHandler.error(exception=e)

    def __get_market_event_repo(self):
        """
        Method to get MarketEvent repository.

        Returns:
            MarketEvent: A MarketEvent repository.
        """
        try:
            return self.db_session.query(MarketEvent)
        except Exception as e:
            self.db_session.rollback()
            return ResponseHandler.error(exception=e)

    def get_market_events(
        self,
        search_term: str = "",
        offset: int = 0,
        limit: int = 10,
    ):
        """
        Method to get MarketEvents with search and pagination.
        """
        try:
            PostAlias = aliased(Post)
            post_exists_subquery = self.db_session.query(literal(True)).filter(
                PostAlias.market_event_id == MarketEvent.id
            ).exists()

            query = self.__get_market_event_repo().with_entities(
                MarketEvent,
                post_exists_subquery.label("post_generated")
            ).filter(
                MarketEvent.processing_status == MarketEvenProcessingtStatus.DRAFTED
            ).order_by(MarketEvent.updated_at.desc())

            if search_term:
                query = query.filter(
                    MarketEvent.title.ilike(f"%{search_term}%") |
                    MarketEvent.description.ilike(f"%{search_term}%")
                )

            total_count = query.count()
            results = query.offset(offset).limit(limit).all()
            return results, total_count

        except Exception as e:
            self.db_session.rollback()
            return ResponseHandler.error(exception=e)

    def get_market_event_by_id(self, id: str) -> MarketEvent | JSONResponse | None:
        """
        Method to get a market_event by id.

        Args:
            user_id (uuid.UUID): MarketEvent id.

        Returns:
            MarketEvent: A MarketEvent object.
        """
        try:
            market_event = self.__get_market_event_repo().get(id)
            return market_event
        except Exception as e:
            self.db_session.rollback()
            return ResponseHandler.error(exception=e)

    def create_market_event(self, market_event_data: MarketEvent):
        """
        Method to create a market_event.

        Args:
            market_event (MarketEvent): A MarketEvent object.

        Returns:
            MarketEvent: A MarketEvent object.
        """
        try:
            self.db_session.add(market_event_data)
            self.db_session.commit()
            self.db_session.refresh(market_event_data)
            return market_event_data
        except Exception as e:
            self.db_session.rollback()
            return ResponseHandler.error(exception=e)

    def update_market_event_by_id(
        self,
        id: str,
        market_event_data: UpdateMarketEventSchema,
    ):
        """
        Update a MarketEvent by its ID.

        Args:
            id (str): ID of the MarketEvent.
            market_event_data (UpdateMarketEventSchema): Data to update the MarketEvent with.

        Returns:
            MarketEvent: The updated MarketEvent object.
        """
        try:
            market_event = self.get_market_event_by_id(id=id)
            update_data = market_event_data.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                setattr(market_event, field, value)

            self.db_session.commit()
            self.db_session.refresh(market_event)
            return market_event
        except Exception as e:
            self.db_session.rollback()
            return ResponseHandler.error(exception=e)

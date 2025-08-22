from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from config.response_handler import ResponseHandler
from src.domain.market_events.models import MarketEvent
from src.domain.market_events.services import MarketEventDomainServices
from src.infrastructure.security import get_current_user_from_token
from src.infrastructure.websockets.connection_manager import ConnectionManager
from src.schema.market_events import MarketEventDataModelSchema, MarketEventResponseSchema


class MarketEventAppServices:
    def __init__(self):
        """
        Constructor for MarketEventAppServices class.

        Initializes a new instance of MarketEventAppServices, which contains
        the application logic for MarketEvents.

        `Attributes:`
        - market_event_domain_services (MarketEventDomainServices): The domain service
          to use for interacting with MarketEvents.
        """
        self.market_event_domain_services = MarketEventDomainServices()

    async def subscribe(self, websocket: WebSocket):
        """
        Endpoint to establish a live websocket connection to receive live MarketEvents.

        This endpoint is used to establish a websocket connection that will receive
        live MarketEvents as they are created. The connection will remain open until
        the client closes it.

        `Args:`
        - websocket (WebSocket): The websocket object to use for the connection.

        `Returns:`
        - None
        """
        token = websocket.query_params.get("token", "")

        current_user = get_current_user_from_token(token=token)

        connection_manager = ConnectionManager()
        await connection_manager.connect(
            websocket=websocket,
            user_id=current_user["user_id"],
        )

        try:
            while True:
                # keep the connection alive
                await websocket.receive_text()
        except WebSocketDisconnect:
            await connection_manager.disconnect(
                websocket=websocket, user_id=current_user["user_id"]
            )
        except Exception as e:
            ResponseHandler.error(exception=e)

    async def get_market_events_listings(
        self,
        current_user: dict,
        search_term: str = "",
        page: int = 1,
        limit: int = 10,
    ) -> MarketEventResponseSchema | JSONResponse:
        """
        Method to get a list of market_events with pagination.
        """
        try:
            offset = (page - 1) * limit
            results, count = self.market_event_domain_services.get_market_events(
                search_term=search_term,
                offset=offset,
                limit=limit,
            )

            # Unpack (market_event_obj, post_generated) and map to schema
            market_event_data = [
                MarketEventDataModelSchema(
                    **market_event.__dict__,
                    post_generated=post_generated,
                )
                for market_event, post_generated in results
            ]

            has_next = offset + limit < count
            has_previous = page > 1
            pages = (count + limit - 1) // limit

            return MarketEventResponseSchema(
                page=page,
                limit=limit,
                total_pages=pages,
                total_records=count,
                has_next=has_next,
                has_previous=has_previous,
                data=market_event_data,
            )
        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def get_market_event_details_by_id(
        self, id: str
    ) -> MarketEvent | JSONResponse | None:
        """
        Method to get a market event by its ID.

        Args:
            id (str): ID of the market event.

        Returns:
            MarketEvent | None: A MarketEvent object if found, else None.
        """
        try:
            market_event = self.market_event_domain_services.get_market_event_by_id(
                id=id
            )
            return market_event
        except Exception as e:
            return ResponseHandler.error(exception=e)

from fastapi import APIRouter, Depends, Query, WebSocket

from config.response_handler import ResponseHandler
from src.application.market_events import MarketEventAppServices
from src.infrastructure.security import get_current_user
from src.schema.market_events import GetMarketEventsResponseSchema
from src.schema.messages_enums import MarketEventEnums

router = APIRouter(
    prefix="/market-events",
    tags=["Market Events"],
)


@router.websocket("/live")
async def websocket_endpoint(websocket: WebSocket):
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
    market_event_app_services = MarketEventAppServices()
    await market_event_app_services.subscribe(websocket=websocket)


@router.get("/", response_model=GetMarketEventsResponseSchema)
async def get_market_events(
    search_term: str = Query("", alias="search"),  # Default empty search term
    page: int = Query(
        1, ge=1
    ),  # Default to page 1, with validation to ensure it's >= 1
    limit: int = Query(
        10, le=100
    ),  # Default to 10 entries per page, with max limit of 100
    current_user: dict = Depends(get_current_user),
):
    """
    Endpoint to retrieve a list of market events with optional search and pagination.

    This endpoint allows clients to retrieve a paginated list of market events.
    Clients can filter the events using a search term and control the pagination
    using page and limit parameters.

    `Args:`
    - search_term (str): An optional term to search for in the market events.
    - page (int): The page number for pagination. Defaults to 1.
    - limit (int): The number of events to return per page. Defaults to 10.
    - current_user (dict): The currently authenticated user.

    `Returns:`
    - GetMarketEventsResponseSchema: A response schema containing the list of market events.
    """

    market_event_app_services = MarketEventAppServices()
    data = await market_event_app_services.get_market_events_listings(
        search_term=search_term,
        page=page,
        limit=limit,
        current_user=current_user,
    )
    return ResponseHandler.success_listings(
        message=MarketEventEnums.MARKET_EVENT_FETCH_SUCCESS,
        data=data,
    )

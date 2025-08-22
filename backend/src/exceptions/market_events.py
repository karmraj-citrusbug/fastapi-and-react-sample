from fastapi import status

from config.exception_handler import BaseHTTPException
from src.schema.messages_enums import MarketEventEnums


class MarketEventNotFoundException(BaseHTTPException):
    def __init__(
        self,
        message: str = MarketEventEnums.MARKET_EVENT_NOT_FOUND.value,
        status_code: int = status.HTTP_404_NOT_FOUND,
    ):
        """
        Constructor for MarketEventNotFoundException class.

        Initializes a new instance of MarketEventNotFoundException, which represents
        an exception that is thrown when a market event is not found.

        `Args:`
        - message (str): The message to return with the exception. Defaults to
          MarketEventEnums.MARKET_EVENT_NOT_FOUND.value.
        - status_code (int): The HTTP status code to return with the exception.
          Defaults to status.HTTP_404_NOT_FOUND.
        """
        super().__init__(message=message, status_code=status_code)

from typing import Any, Optional
import logging

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from config.exception_handler import BaseHTTPException

logger = logging.getLogger("app.errors")


class ResponseHandler:
    """
    Custom response handler for consistent API responses.
    """

    @staticmethod
    def success(
        status_code: int = status.HTTP_200_OK,
        message: str = "Success",
        data: Optional[Any] = None,
    ) -> JSONResponse:
        """
        Standardized success response.
        """
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(
                {
                    "success": True,
                    "status_code": status_code,
                    "message": message,
                    "data": data,
                }
            ),
        )

    @staticmethod
    def success_listings(
        status_code: int = status.HTTP_200_OK,
        message: str = "Success",
        data: Any = [],
    ) -> JSONResponse:
        """
        Standardized success response for listing data.
        """
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(
                {
                    "success": True,
                    "status_code": status_code,
                    "message": message,
                    "page": data.page,
                    "limit": data.limit,
                    "total_pages": data.total_pages,
                    "total_records": data.total_records,
                    "has_next": data.has_next,
                    "has_previous": data.has_previous,
                    "data": data.data,
                }
            ),
        )

    @staticmethod
    def error(
        exception: Exception,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        message: str = "Something went wrong",
    ) -> JSONResponse:
        """
        Standardized error response.
        """

        if isinstance(exception, BaseHTTPException):
            raise exception

        logger.exception("Unhandled exception: %s", str(exception))

        raise BaseHTTPException(status_code=status_code, message=message)

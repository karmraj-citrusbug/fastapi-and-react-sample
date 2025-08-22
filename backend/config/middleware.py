import json
import logging
from uuid import uuid4

from fastapi import HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class UUIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        """
        A middleware that assigns a unique UUID to each request and logs the request and response.

        This middleware assigns a unique UUID to each request and stores it in the request state.
        It also logs the request method and URL, as well as the status code of the response.

        :param request: The incoming request
        :param call_next: The next middleware in the chain
        :return: The response to the request
        """

        logger = logging.getLogger("app.request")
        request_id = str(uuid4())
        request.state.request_id = request_id
        logger.info("Request %s: %s %s", request_id, request.method, request.url)
        response = await call_next(request)
        logger.info("Response %s: status_code=%s", request_id, response.status_code)
        return response


async def validation_exception_handling_middleware(
    request: Request, exc: RequestValidationError
):
    """
    This exception handler catches RequestValidationError exceptions and returns a JSONResponse
    with a 422 status code and a JSON body containing the validation errors.

    :param request: The incoming request
    :param exc: The RequestValidationError exception
    :return: A JSONResponse with a 422 status code and a JSON body
    """

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "Invalid payload",
        },
    )


async def http_exception_handling_middleware(request: Request, exc: HTTPException):
    """
    This exception handler catches StarletteHTTPException exceptions and returns a JSONResponse
    with a status code and a JSON body containing the error detail.

    :param request: The incoming request
    :param exc: The StarletteHTTPException exception
    :return: A JSONResponse with a status code and a JSON body containing the error detail
    """

    if exc.detail[0] == "{":
        return JSONResponse(status_code=exc.status_code, content=json.loads(exc.detail))
    else:
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder(
                {
                    "success": False,
                    "status_code": exc.status_code,
                    "message": exc.detail,
                    "data": None,
                }
            ),
        )

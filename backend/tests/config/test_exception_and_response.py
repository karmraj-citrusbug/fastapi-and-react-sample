import json

from fastapi import status

from config.exception_handler import BaseHTTPException
from config.response_handler import ResponseHandler


def test_base_http_exception_detail_format():
    exc = BaseHTTPException(message="X", status_code=status.HTTP_418_IM_A_TEAPOT)
    payload = json.loads(exc.detail)
    assert payload["success"] is False
    assert payload["status_code"] == status.HTTP_418_IM_A_TEAPOT
    assert payload["message"] == "X"


def test_response_handler_success_structure():
    resp = ResponseHandler.success(message="ok", data={"a": 1})
    assert resp.status_code == status.HTTP_200_OK
    body = json.loads(resp.body.decode())
    assert body["success"] is True and body["data"] == {"a": 1}


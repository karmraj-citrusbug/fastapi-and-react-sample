from fastapi import status

from config.exception_handler import BaseHTTPException
from src.schema.messages_enums import AuthEnums


class UserNotFoundException(BaseHTTPException):
    def __init__(
        self,
        message: str = AuthEnums.USER_NOT_FOUND.value,
        status_code: int = status.HTTP_404_NOT_FOUND,
    ):
        """
        Constructor for UserNotFoundException class.

        Initializes a new instance of UserNotFoundException, which represents
        an exception that is thrown when a user is not found.

        `Args:`
        - message (str): The message to return with the exception. Defaults to
          AuthEnums.USER_NOT_FOUND.value.
        - status_code (int): The HTTP status code to return with the exception.
          Defaults to status.HTTP_404_NOT_FOUND.
        """
        super().__init__(message=message, status_code=status_code)


class AuthenticationException(BaseHTTPException):
    def __init__(
        self,
        message: str = AuthEnums.INVALID_EMAIL_OR_PASSWORD.value,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        """
        Constructor for AuthenticationException class.

        Initializes a new instance of AuthenticationException, which represents
        an exception that is thrown when authentication fails.

        `Args:`
        - message (str): The message to return with the exception. Defaults to
          AuthEnums.INVALID_EMAIL_OR_PASSWORD.value.
        - status_code (int): The HTTP status code to return with the exception.
          Defaults to status.HTTP_401_UNAUTHORIZED.
        """
        super().__init__(message=message, status_code=status_code)


class UserAlreadyExistsException(BaseHTTPException):
    def __init__(
        self,
        message: str = AuthEnums.USER_ALREADY_EXIST.value,
        status_code: int = status.HTTP_409_CONFLICT,
    ):
        """
        Constructor for UserAlreadyExistsException class.

        Initializes a new instance of UserAlreadyExistsException, which represents
        an exception that is thrown when a user already exists.

        `Args:`
        - message (str): The message to return with the exception. Defaults to
          AuthEnums.USER_ALREADY_EXIST.value.
        - status_code (int): The HTTP status code to return with the exception.
          Defaults to status.HTTP_409_CONFLICT.
        """
        super().__init__(message=message, status_code=status_code)


class EmailServiceException(BaseHTTPException):
    def __init__(
        self,
        message: str = AuthEnums.EMAIL_SERVICE_ERROR.value,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        """
        Constructor for EmailServiceException class.

        Initializes a new instance of EmailServiceException, which represents
        an exception that is thrown when a problem occurs while sending an email.

        `Args:`
        - message (str): The message to return with the exception. Defaults to
          AuthEnums.EMAIL_SERVICE_ERROR.value.
        - status_code (int): The HTTP status code to return with the exception.
          Defaults to status.HTTP_500_INTERNAL_SERVER_ERROR.
        """
        super().__init__(message=message, status_code=status_code)

from fastapi import status

from config.exception_handler import BaseHTTPException
from src.schema.messages_enums import GeneralEnums, PostEnums


class PostNotFoundException(BaseHTTPException):
    def __init__(
        self,
        message: str = PostEnums.POST_NOT_FOUND.value,
        status_code: int = status.HTTP_404_NOT_FOUND,
    ):
        """
        Constructor for PostNotFoundException class.

        Initializes a new instance of PostNotFoundException, which represents
        an exception that is thrown when a post is not found.

        `Args:`
        - message (str): The message to return with the exception. Defaults to
          PostEnums.POST_NOT_FOUND.value.
        - status_code (int): The HTTP status code to return with the exception.
          Defaults to status.HTTP_404_NOT_FOUND.
        """
        super().__init__(message=message, status_code=status_code)


class PostNotAuthorizedException(BaseHTTPException):
    def __init__(
        self,
        message: str = GeneralEnums.NOT_AUTHORIZED.value,
        status_code: int = status.HTTP_403_FORBIDDEN,
    ):
        """
        Constructor for PostNotAuthorizedException class.

        Initializes a new instance of PostNotAuthorizedException, which represents
        an exception that is thrown when a user is not authorized to access a post.

        `Args:`
        - message (str): The message to return with the exception. Defaults to
          GeneralEnums.NOT_AUTHORIZED.value.
        - status_code (int): The HTTP status code to return with the exception.
          Defaults to status.HTTP_403_FORBIDDEN.
        """
        super().__init__(message=message, status_code=status_code)


class PostNotDraftedException(BaseHTTPException):
    def __init__(
        self,
        message: str = PostEnums.POST_NOT_DRAFTED.value,
        status_code: int = status.HTTP_403_FORBIDDEN,
    ):
        """
        Constructor for PostNotDraftedException class.

        Initializes a new instance of PostNotDraftedException, which represents
        an exception that is thrown when a post is not in draft state.

        `Args:`
        - message (str): The message to return with the exception. Defaults to
          PostEnums.POST_NOT_DRAFTED.value.
        - status_code (int): The HTTP status code to return with the exception.
          Defaults to status.HTTP_403_FORBIDDEN.
        """
        super().__init__(message=message, status_code=status_code)


class PostNotPublishedException(BaseHTTPException):
    def __init__(
        self,
        message: str = PostEnums.POST_NOT_PUBLISHED.value,
        status_code: int = status.HTTP_403_FORBIDDEN,
    ):
        """
        Constructor for PostNotPublishedException class.

        Initializes a new instance of PostNotPublishedException, which represents
        an exception that is thrown when a post is not published.

        `Args:`
        - message (str): The message to return with the exception. Defaults to
          PostEnums.POST_NOT_PUBLISHED.value.
        - status_code (int): The HTTP status code to return with the exception.
          Defaults to status.HTTP_403_FORBIDDEN.
        """
        super().__init__(message=message, status_code=status_code)

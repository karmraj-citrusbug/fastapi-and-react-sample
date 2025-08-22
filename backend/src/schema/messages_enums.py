from enum import Enum


class AuthEnums(str, Enum):
    SIGN_UP_SUCCESS = (
        "User registered successfully. A verification email has been sent."
    )
    LOGIN_SUCCESS = "User authenticated successfully"
    FORGOT_PASSWORD_EMAIL_SENT_SUCCESS = "Password reset email sent successfully."
    RESET_PASSWORD_SUCCESS = "Password reset completed successfully."
    PASSWORD_CHANGED_SUCCESS = "Password changed successfully."
    EMAIL_VERIFICATION_SUCCESS = "Email verified successfully."
    EMAIL_SERVICE_ERROR = "Email service error"

    USER_NOT_FOUND = "User not found"
    INVALID_EMAIL_OR_PASSWORD = "Invalid email or password"
    USER_ALREADY_EXIST = "User already exists"


class GeneralEnums(str, Enum):
    INTERNAL_SERVER_ERROR = "Internal server error"
    NOT_AUTHORIZED = "You are not authorized to perform this action"


class UserEnums(str, Enum):
    USER_FETCH_SUCCESS = "User profile retrieved successfully"
    USER_UPDATE_SUCESS = "User profile updated successfully"


class MarketEventEnums(str, Enum):
    MARKET_EVENT_FETCH_SUCCESS = "Market event fetched successfully"
    MARKET_EVENT_NOT_FOUND = "Market event not found"


class PostEnums(str, Enum):
    POST_FETCH_SUCCESS = "Post fetched successfully"
    POST_NOT_FOUND = "Post not found"
    POST_UPDATE_SUCCESS = "Post updated successfully"
    POST_CREATE_SUCCESS = "Post created successfully"
    POST_APPROVE_SUCCESS = "Post approved successfully"
    POST_PUBLISH_SUCCESS = "Posts published successfully"
    POST_CUSTOMIZE_SUCCESS = "Post customized successfully"
    CUSTOMIZE_POST_SUCCESS = "Customized post created successfully"
    POST_STATISTICS_SUCCESS = "Post statistics fetched successfully"
    POST_NOT_DRAFTED = "Post is not drafted"
    POST_NOT_PUBLISHED = "Post is not published"

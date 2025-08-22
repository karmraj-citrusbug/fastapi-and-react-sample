import re
from datetime import UTC, datetime, timedelta
from typing import Dict, Optional

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext

from config.response_handler import ResponseHandler
from config.settings import app_settings as settings
from src.exceptions.users import AuthenticationException

# Password validation constants
MIN_PASSWORD_LENGTH = 8
REQUIRE_SPECIAL_CHAR = True
REQUIRE_NUMBER = True
REQUIRE_UPPERCASE = True
REQUIRE_LOWERCASE = True

# Create a CryptContext for password hashing with stronger settings
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,  # Increased rounds for better security
)


def validate_password_strength(password: str) -> bool:
    """
    Validates password strength against security requirements.

    Args:
        password (str): The password to validate.

    Returns:
        bool: True if password meets requirements, False otherwise.

    Raises:
        ValueError: If password doesn't meet requirements, with specific reason.
    """
    # STRONG_PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?\":{}|<>]).{8,}$"

    requirements = {
        "Password must be at least 8 characters long": len(password)
        >= MIN_PASSWORD_LENGTH,
        "Password must contain at least one special character": bool(
            re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
        )
        if REQUIRE_SPECIAL_CHAR
        else True,
        "Password must contain at least one number": bool(re.search(r"\d", password))
        if REQUIRE_NUMBER
        else True,
        "Password must contain at least one uppercase letter": bool(
            re.search(r"[A-Z]", password)
        )
        if REQUIRE_UPPERCASE
        else True,
        "Password must contain at least one lowercase letter": bool(
            re.search(r"[a-z]", password)
        )
        if REQUIRE_LOWERCASE
        else True,
    }

    failed_checks = [msg for msg, passed in requirements.items() if not passed]

    if failed_checks:
        raise AuthenticationException(
            f"Please enter strong password having: \n {'\n'.join(f'"{msg}"' for msg in failed_checks)}"
        )

    return True


def hash_password(password: str):
    """
    Hashes a password using bcrypt after validating its strength.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.

    Raises:
        ValueError: If password doesn't meet strength requirements.
    """
    validate_password_strength(password)
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password against its hash using constant-time comparison.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


class TokenServices:
    """
    Service class for handling JWT token operations.
    """

    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.reset_token_expiry_hours = settings.RESET_TOKEN_EXPIRY_HOURS
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def generate_access_token(
        self, user_id: str, additional_claims: Optional[Dict] = None
    ):
        """
        Generate a JWT access token with enhanced security.

        Args:
            user_id (str): User ID.
            additional_claims (Optional[Dict]): Additional claims to include in token.

        Returns:
            str: Encoded JWT token.

        Raises:
            AuthenticationException: If token generation fails.
        """
        try:
            expiration = datetime.now(UTC) + timedelta(
                minutes=self.access_token_expire_minutes
            )
            payload = {
                "user_id": user_id,
                "exp": expiration,
                "iat": datetime.now(UTC),
                "type": "access",
            }

            if additional_claims:
                payload.update(additional_claims)

            return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        except Exception as e:
            return ResponseHandler.error(
                exception=e,
                message="Access token generation failed",
            )

    def generate_verification_token(
        self, user_id: str, token_type: str = "verification"
    ):
        """
        Generate a verification token for a user with specified type.

        Args:
            user_id (str): The ID of the user.
            token_type (str): Type of token (verification/reset).

        Returns:
            str: A JWT token.

        Raises:
            AuthenticationException: If token generation fails.
        """
        try:
            expiry = datetime.now(UTC) + timedelta(hours=self.reset_token_expiry_hours)
            payload = {
                "sub": str(user_id),
                "exp": expiry,
                "type": token_type,
                "iat": datetime.now(UTC),
            }
            return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        except Exception as e:
            return ResponseHandler.error(
                exception=e,
                message="Verification token generation failed",
            )

    def verify_token(self, token: str, expected_type: str | None = None):
        """
        Verify and decode a JWT token.

        Args:
            token (str): The JWT token.
            expected_type (str, optional): Expected token type.

        Returns:
            dict: The decoded token payload.

        Raises:
            AuthenticationException: If token is invalid or expired.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            if expected_type and payload.get("type") != expected_type:
                raise AuthenticationException(
                    f"Invalid token type. Expected {expected_type}"
                )

            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationException("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationException("Invalid token")
        except Exception as e:
            return ResponseHandler.error(
                exception=e, message="Token verification failed"
            )

    def verify_reset_token(self, token: str):
        """
        Verify the reset password token.

        Args:
            token (str): The JWT token.

        Returns:
            str: The user ID if the token is valid.

        Raises:
            AuthenticationException: If token is invalid or expired.
        """
        try:
            payload = self.verify_token(token, expected_type="reset")
            user_id = payload.get("sub")
            if not user_id:
                raise AuthenticationException("Invalid reset token: missing user ID")
            return user_id
        except Exception as e:
            return ResponseHandler.error(
                exception=e,
                message="Reset token verification failed",
            )


# Create a global instance of TokenServices
token_services = TokenServices()

# Instantiate HTTPBearer to use it for token authorization
security_bearer_schema = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_bearer_schema),
):
    """
    Get current authenticated user from token.

    Args:
        token (str): JWT token.

    Returns:
        dict: User data from token.

    Raises:
        AuthenticationException: If token is invalid.
    """

    try:
        return token_services.verify_token(token=credentials.credentials)
    except Exception as e:
        return ResponseHandler.error(exception=e)


def get_current_user_from_token(token: str):
    """
    Get current authenticated user from token.

    Args:
        token (str): JWT token.

    Returns:
        dict: User data from token.

    Raises:
        AuthenticationException: If token is invalid.
    """

    try:
        return token_services.verify_token(token=token)
    except Exception as e:
        return ResponseHandler.error(exception=e)

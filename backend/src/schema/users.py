from typing import Optional
from uuid import UUID

from fastapi import status
from pydantic import BaseModel, ConfigDict, EmailStr


class UserDataModelSchema(BaseModel):
    """
    Schema for user data.
    """

    id: UUID
    username: str
    email: EmailStr
    is_verified: bool
    password: str
    created_at: str
    updated_at: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426655440000",
                "username": "johndoe",
                "email": "johndoe@example.com",
                "is_verified": False,
                "password": "securepassword123",
                "created_at": "2021-01-01T00:00:00Z",
                "updated_at": "2021-01-01T00:00:00Z",
            }
        }
    )


class UserResponseSchema(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_verified: bool

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426655440000",
                "username": "johndoe",
                "email": "johndoe@example.com",
                "is_verified": False,
            }
        }
    )


class TokenPayload(BaseModel):
    token: str


class ForgotPasswordRequestSchema(BaseModel):
    email: EmailStr


class ResetPasswordRequestSchema(BaseModel):
    token: str
    new_password: str


class SignupUserRequestSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password": "securepassword123",
            }
        }
    )


class LoginUserRequestSchema(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "johndoe@example.com",
                "password": "securepassword123",
            }
        }
    )


class SignUpResponseSchema(BaseModel):
    success: bool = True
    status_code: int = status.HTTP_200_OK
    message: str = "User registered successfully. A verification email has been sent."
    data: UserResponseSchema

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "status_code": 200,
                "message": "User registered successfully. A verification email has been sent.",
                "data": {
                    "id": "123e4567-e89b-12d3-a456-426655440000",
                    "username": "johndoe",
                    "email": "johndoe@example.com",
                    "is_verified": False,
                },
            }
        }
    )


class LoginResponseModel(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "token",
                "token_type": "bearer",
            }
        }
    )


class LoginResponseSchema(BaseModel):
    success: bool = True
    status_code: int = status.HTTP_200_OK
    message: str = "User authenticated successfully"
    data: LoginResponseModel

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "status_code": 200,
                "message": "User authenticated successfully",
                "data": {
                    "access_token": "token",
                    "token_type": "bearer",
                },
            }
        }
    )


class UserProfileResponseSchema(BaseModel):
    """
    Schema for user profile response.
    """

    success: bool = True
    status_code: int = status.HTTP_200_OK
    message: str = "User profile retrieved successfully"
    data: UserResponseSchema


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "old_password": "securepassword123",
                "new_password": "newsecurepassword123",
            }
        }
    )


class UpdateUserDomainSchema(BaseModel):
    username: Optional[str] = None
    is_verified: Optional[bool] = None
    password: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "is_verified": True,
                "password": "securepassword123",
            }
        }
    )


class UpdateUserRequestSchema(BaseModel):
    username: Optional[str]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe",
            }
        }
    )


class ForgotPasswordResponseSchema(BaseModel):
    success: bool = True
    status_code: int = status.HTTP_200_OK
    message: str = "Password reset email sent successfully."
    data: None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "status_code": 200,
                "message": "Password reset email sent successfully.",
                "data": None,
            }
        }
    )


class ResetPasswordResponseSchema(BaseModel):
    success: bool = True
    status_code: int = status.HTTP_200_OK
    message: str = "Password reset completed successfully"
    data: None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "status_code": 200,
                "message": "Password reset completed successfully",
                "data": None,
            }
        }
    )


class ChangePasswordResponseSchema(BaseModel):
    success: bool = True
    status_code: int = status.HTTP_200_OK
    message: str = "Password changed successfully"
    data: None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "status_code": 200,
                "message": "Password changed successfully",
                "data": None,
            }
        }
    )


class UpdateUserResponseSchema(BaseModel):
    """
    Schema for update user.
    """

    success: bool = True
    status_code: int = status.HTTP_200_OK
    message: str = "User profile updated successfully"
    data: UserResponseSchema


class VerifyEmailResponseSchema(BaseModel):
    success: bool = True
    status_code: int = status.HTTP_200_OK
    message: str = "Email verified successfully"
    data: UserResponseSchema


class UserLoginResponseSchema(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "token",
                "token_type": "bearer",
            }
        }
    )

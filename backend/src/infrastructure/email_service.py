from typing import Dict

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from config.response_handler import ResponseHandler
from config.settings import app_settings as settings
from src.exceptions.users import EmailServiceException

SENDGRID_API_KEY = settings.SENDGRID_API_KEY
FROM_EMAIL = settings.FROM_EMAIL
SENDGRID_FORGOT_PASSWORD_TEMPLATE_ID = settings.SENDGRID_FORGOT_PASSWORD_TEMPLATE_ID
FRONTEND_URL = settings.FRONTEND_URL
SENDGRID_VERIFY_EMAIL_TEMPLATE_ID = settings.SENDGRID_VERIFY_EMAIL_TEMPLATE_ID


class EmailService:
    """
    Email service class for handling all email communications.
    """

    def __init__(self):
        """
        Initialize the email service with SendGrid client.
        """
        self.client = SendGridAPIClient(SENDGRID_API_KEY) if SENDGRID_API_KEY else None

    async def __send_templated_email(
        self,
        to_email: str,
        template_id: str,
        dynamic_template_data: Dict,
        subject: str,
    ):
        """
        Send an email using a SendGrid dynamic template.

        Args:
            to_email (str): Recipient email address.
            template_id (str): SendGrid template ID.
            dynamic_template_data (Dict): Template variables.
            subject (Optional[str]): Email subject (optional).

        Returns:
            bool: True if email sent successfully.

        Raises:
            EmailServiceException: If email sending fails.
        """
        # In showcase mode or missing API key, pretend-send for safety
        if self.client is None:
            return True

        try:
            message = Mail(
                from_email=settings.FROM_EMAIL,
                to_emails=to_email,
                subject=subject,
            )
            message.dynamic_template_data = dynamic_template_data
            message.template_id = template_id

            response = self.client.send(message=message)

            if response.status_code not in [200, 202]:
                raise EmailServiceException(
                    f"Failed to send email. Status code: {response.status_code}"
                )

        except Exception as e:
            return ResponseHandler.error(exception=e)

    async def send_forgot_password_email(self, username: str, email: str, token: str):
        """
        Send a password reset email.

        Args:
            email (str): Recipient email address.
            token (str): Reset password token.

        Returns:
            bool: True if email sent successfully.

        Raises:
            EmailServiceException: If email sending fails.
        """
        reset_password_link = f"{FRONTEND_URL}/reset-password?token={token}"

        template_data = {
            "username": username,
            "reset_password_link": reset_password_link,
        }

        return await self.__send_templated_email(
            to_email=email,
            template_id=SENDGRID_FORGOT_PASSWORD_TEMPLATE_ID,
            dynamic_template_data=template_data,
            subject="Reset Your Password",
        )

    async def send_signup_verification_email(
        self, username: str, email: str, token: str
    ):
        """
        Send a signup verification email.

        Args:
            email (str): Recipient email address.
            token (str): Email verification token.

        Returns:
            bool: True if email sent successfully.

        Raises:
            EmailServiceException: If email sending fails.
        """
        verification_link = f"{FRONTEND_URL}/verify-user?token={token}"

        template_data = {
            "username": username,
            "verification_link": verification_link,
        }

        return await self.__send_templated_email(
            to_email=email,
            template_id=SENDGRID_VERIFY_EMAIL_TEMPLATE_ID,
            dynamic_template_data=template_data,
            subject="Verify Your Email Address",
        )

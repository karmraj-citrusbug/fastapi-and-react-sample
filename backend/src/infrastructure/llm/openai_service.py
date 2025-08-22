import json
import logging
from typing import List, Optional

from openai import OpenAI, OpenAIError

from config.settings import app_settings
from src.schema.utils import PromptEnum

logger = logging.getLogger(__name__)


class OpenAIServices:
    def __init__(self):
        self.client = None
        try:
            api_key = app_settings.OPENAI_API_KEY
            if api_key:
                self.client = OpenAI(api_key=api_key)
                logger.info("OpenAI client initialized successfully.")
            else:
                logger.warning(
                    "OPENAI_API_KEY not set. OpenAI calls will return stubbed responses."
                )
        except Exception as e:
            logger.error("Failed to initialize OpenAI client: %s", e)
            self.client = None

    def _build_messages(
        self,
        user_prompt: str,
        system_prompt: Optional[PromptEnum],
    ) -> List[dict]:
        """
        Builds the message payload for the OpenAI API.

        Args:
            user_prompt (str): The user's input prompt.
            system_prompt (Optional[str]): The system's context or instructions.

        Returns:
            List[dict]: A list of message dictionaries for the OpenAI API.
        """

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt.value})
        if user_prompt:
            messages.append({"role": "user", "content": user_prompt})
        return messages

    def get_chat_completion(
        self,
        user_prompt: str,
        system_prompt: Optional[PromptEnum] = None,
        model: str = "gpt-4o-mini",
    ) -> str | dict:
        """
        Generates a chat completion response using OpenAI's API.

        Args:
            user_prompt (str): The user's input prompt.
            system_prompt (Optional[str]): The system's context or instructions.
            model (str): The OpenAI model to use (default: "gpt-4o-mini").

        Returns:
            str: The response content from the OpenAI API.

        Raises:
            OpenAIError: If the API call fails.
        """

        messages = self._build_messages(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
        )

        # Return a deterministic stub if client is not configured
        if self.client is None:
            logger.info("Returning stubbed OpenAI response for prompt: %s", user_prompt)
            return {
                "summary": "Stubbed response (no API key configured).",
                "input": user_prompt,
                "model": model,
            }

        try:
            logger.debug("Sending request to OpenAI with model: %s", model)
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
            )
            logger.info("Received response from OpenAI.")
            result = response.choices[0].message.content.strip()
            return json.loads(result) if result.startswith("{") else result
        except OpenAIError as e:
            logger.error("OpenAI API error: %s", e, e.__traceback__.tb_lineno)
            raise
        except Exception as e:
            logger.error(
                "Unexpected error during OpenAI API call: %s",
                e,
                e.__traceback__.tb_lineno,
            )
            raise

import json
import logging

from src.infrastructure.llm.openai_service import OpenAIServices
from src.schema.utils import PromptEnum

logger = logging.getLogger(__name__)


class NewsFetcherLLMService:
    def __init__(self):
        self.openai_services = OpenAIServices()

    def classify_financial_data(self, article: dict):
        response = self.openai_services.get_chat_completion(
            system_prompt=PromptEnum.FINANCIAL_DATA_SYSTEM_PROMPT,
            user_prompt=f"{json.dumps(article)}.\nNOTE [IMPORTANT]: Make sure to provide the JSON response only.",
        )

        if isinstance(response, str):
            logger.info("Classification is not a fetched as dictionary and retrying...")
            response = self.openai_services.get_chat_completion(
                system_prompt=PromptEnum.FINANCIAL_DATA_SYSTEM_PROMPT,
                user_prompt=f"{json.dumps(article)}.\nNOTE [IMPORTANT]: Make sure to provide the JSON response only.",
            )
        else:
            return response

    def generate_event_title(self, article: dict):
        result = self.openai_services.get_chat_completion(
            system_prompt=PromptEnum.GENERATE_EVENT_TITLE_SYSTEM_PROMPT,
            user_prompt=f"{json.dumps(article)}",
        )
        return result

    def get_deep_researched_content(self, article: dict):
        result = self.openai_services.get_chat_completion(
            system_prompt=PromptEnum.GENERATE_DEEP_RESEARCHED_CONTENT_SYSTEM_PROMPT,
            user_prompt=f"{json.dumps(article)}",
        )
        return result

    def fetch_summarized_content_from_deep_research(
        self,
        deep_research_content: str,
    ):
        result = self.openai_services.get_chat_completion(
            system_prompt=PromptEnum.GENERATE_SUMMARIZED_CONTENT_FROM_DEEP_RESEARCH_SYSTEM_PROMPT,
            user_prompt=deep_research_content,
        )
        return result

    def fetch_sentimental_analysis(self, article: dict):
        result = self.openai_services.get_chat_completion(
            system_prompt=PromptEnum.GET_SENTIMENTAL_ANALYSIS_SYSTEM_PROMPT,
            user_prompt=f"{json.dumps(article)}",
        )
        return result

    def fetch_priority_flag(self, article: dict):
        result = self.openai_services.get_chat_completion(
            system_prompt=PromptEnum.GET_PRIORITY_FLAG_SYSTEM_PROMPT,
            user_prompt=f"{json.dumps(article)}",
        )
        return result

    def fetch_compliance_check(self, article: dict):
        result = self.openai_services.get_chat_completion(
            system_prompt=PromptEnum.GET_COMPLIANCE_CHECK_SYSTEM_PROMPT,
            user_prompt=f"{json.dumps(article)}",
        )
        return result

    def generate_keyword_combinations(self, title: str) -> list[str]:
        """
        Generate intelligent keyword combinations using OpenAI.

        Args:
            title (str): The event title to generate combinations from

        Returns:
            list[str]: List of keyword combinations
        """

        system_prompt = """You are a financial news search expert. Your task is to generate a list of relevant search keywords and phrases from a given title.
            The keywords should:
            1. Include important terms and their variations
            2. Include relevant financial/market terms that are implied but not directly mentioned
            3. Include company names, ticker symbols, and industry terms if applicable
            4. Be ordered from most specific to most general

            Return ONLY a JSON array of strings, with each string being a search keyword or phrase."""

        user_prompt = f"Generate search keywords for the title: {title}"

        try:
            response = self.openai_services.get_chat_completion(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )

            # Parse the response as JSON array
            if isinstance(response, str):
                try:
                    keywords = json.loads(response)
                    if isinstance(keywords, list):
                        return keywords
                except json.JSONDecodeError:
                    # If response isn't valid JSON, try to extract keywords by splitting
                    return [
                        kw.strip()
                        for kw in response.replace("[", "").replace("]", "").split(",")
                        if kw.strip()
                    ]

            return []

        except Exception as e:
            print(f"Error generating keywords: {e}")
            # Fallback to simple title words if OpenAI fails
            return [title]

    def research_customized_content(self, articles: list):
        result = self.openai_services.get_chat_completion(
            system_prompt=PromptEnum.GENERATE_DEEP_RESEARCHED_CONTENT_SYSTEM_PROMPT,
            user_prompt=f"{json.dumps(articles)}",
        )
        return result

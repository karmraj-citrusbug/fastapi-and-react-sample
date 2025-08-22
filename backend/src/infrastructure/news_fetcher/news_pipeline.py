import logging

from src.domain.enums import PriorityFlag, SentimentalAnalysis
from src.infrastructure.news_fetcher.core.event_registry_news_fetcher import (
    EventRegistryNewsFetcher,
)
from src.infrastructure.news_fetcher.news_fetcher_llm_services import (
    NewsFetcherLLMService,
)

logger = logging.getLogger(__name__)


class NewsPipeline:
    """
    Step 1: Save the classified financial data to the database and broadcast it
    Step 2: Generate the title like AI researching {title}
    Step 3: Assign for deep researching and analysis to perplexity (status: researching)
    Step 4: Fetch the content source of the classified financial data and broadcast it (status: researching)
    Step 5: Fetch the deep_research and summarize it as per the best content (status: writing)
    Step 6: Fetch the sentimental analysis of the classified financial data and broadcast it (status: analyzing sentiment)
    Step 7: Fetch the priority flag of the classified financial data and broadcast it (status: assigning priority)
    Step 8: Fetch the compliance check status of the classified financial data and broadcast it (status: checking compliance)
    """

    def __init__(self):
        self.news_fetcher_llm_services = NewsFetcherLLMService()
        self.event_registry_news_fetcher = EventRegistryNewsFetcher()

    def classify_financial_article(self, article: dict):
        logger.info(f"\nClassifying financial article: {article.get('title')}")
        return self.news_fetcher_llm_services.classify_financial_data(article)

    def generate_ai_processing_title(self, article: dict):
        logger.info(
            f"\nGenerating AI processing title for article: {article.get('title')}"
        )
        return self.news_fetcher_llm_services.generate_event_title(article)

    def deep_research_financial_article(self, article: dict):
        logger.info(f"\nDeep researching financial article: {article.get('title')}")
        return self.news_fetcher_llm_services.get_deep_researched_content(article)

    def fetch_summarized_content_from_deep_research(self, deep_research_content: str):
        logger.info("\nFetching summarized content from deep research for article")
        return (
            self.news_fetcher_llm_services.fetch_summarized_content_from_deep_research(
                deep_research_content=deep_research_content
            )
        )

    def fetch_sentimental_analysis(self, article: dict) -> SentimentalAnalysis | None:
        logger.info(
            f"\nFetching sentimental analysis for article: {article.get('title')}"
        )
        sentimental_analysis = (
            self.news_fetcher_llm_services.fetch_sentimental_analysis(article)
        )
        match sentimental_analysis:
            case SentimentalAnalysis.POSITIVE.value:
                sentimental_analysis = SentimentalAnalysis.POSITIVE
            case SentimentalAnalysis.NEGATIVE.value:
                sentimental_analysis = SentimentalAnalysis.NEGATIVE
            case SentimentalAnalysis.NEUTRAL.value:
                sentimental_analysis = SentimentalAnalysis.NEUTRAL
            case _:
                sentimental_analysis = None
        return sentimental_analysis

    def fetch_priority_flag(self, article: dict) -> PriorityFlag | None:
        logger.info(f"\nFetching priority flag for article: {article.get('title')}")
        priority_flag = self.news_fetcher_llm_services.fetch_priority_flag(article)
        match priority_flag:
            case PriorityFlag.HIGH.value:
                priority_flag = PriorityFlag.HIGH
            case PriorityFlag.MEDIUM.value:
                priority_flag = PriorityFlag.MEDIUM
            case PriorityFlag.LOW.value:
                priority_flag = PriorityFlag.LOW
            case _:
                priority_flag = None
        return priority_flag

    def fetch_compliance_check(self, article: dict):
        logger.info(f"\nFetching compliance check for article: {article.get('title')}")
        return self.news_fetcher_llm_services.fetch_compliance_check(article)

    def generate_keyword_combinations(self, title: str):
        return self.news_fetcher_llm_services.generate_keyword_combinations(title)

    def research_customized_content(self, articles: list):
        logger.info("\nDeep researching customized content for articles")
        return self.news_fetcher_llm_services.research_customized_content(articles)

    async def fetch_news_by_title(self, title: str) -> list:
        """
        Fetches news articles by trying different keyword combinations from a title.

        Args:
            title (str): The event title to search for

        Returns:
            list: Combined list of relevant articles
        """
        all_articles = []
        seen_urls = set()

        # Generate keyword combinations using OpenAI
        keyword_combinations = self.generate_keyword_combinations(title=title)

        # Try each combination
        for keyword in keyword_combinations:
            articles = await self.event_registry_news_fetcher.fetch_news(
                keyword=keyword
            )

            # Add only unique articles based on URL
            for article in articles:
                url = article.get("url")
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    all_articles.append(article)

        return all_articles

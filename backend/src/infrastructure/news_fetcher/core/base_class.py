from abc import ABC, abstractmethod


class NewsFetcherBase(ABC):
    @abstractmethod
    async def fetch_news(self):
        """
        Fetch news articles from the third-party API.

        Returns:
            List[Dict]: A list of news articles.
        """
        pass

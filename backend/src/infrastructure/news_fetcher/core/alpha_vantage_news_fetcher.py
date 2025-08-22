import random

import httpx

from config.settings import app_settings
from src.infrastructure.news_fetcher.core.base_class import NewsFetcherBase
from src.infrastructure.utils import get_time_range
from src.schema.utils import GetTimeRangeResponseDTO
from static import NEWS_STATIC_DATA


class AlphaVantageNewsFetcher(NewsFetcherBase):
    async def fetch_news(self):
        """
        Fetches news data from Alpha Vantage API.

        Returns:
            list: A list of news articles.
        """

        if app_settings.FETCH_STATIC_DATA:
            data = NEWS_STATIC_DATA.get("feed", [])
            response = random.sample(data, 30)
        else:
            time_ranges: GetTimeRangeResponseDTO = get_time_range()

            params = {
                "function": "NEWS_SENTIMENT",
                "apikey": app_settings.ALPHAVANTAGE_API_KEY,
                "time_from": time_ranges.time_from,
                "limit": 1000,
            }

            with httpx.Client(timeout=15) as client:
                response = client.get(
                    f"{app_settings.ALPHAVANTAGE_API_BASE_URL}/query",
                    params=params,
                )
                response.raise_for_status()

            data: dict = response.json()
            response = data.get("feed", [])
        return response

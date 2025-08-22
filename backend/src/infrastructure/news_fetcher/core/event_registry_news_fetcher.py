import random
from datetime import UTC, datetime
from typing import Optional

import httpx

from config.settings import app_settings
from src.infrastructure.news_fetcher.core.base_class import NewsFetcherBase
from static import NEWS_STATIC_DATA


class EventRegistryNewsFetcher(NewsFetcherBase):
    async def fetch_news(self, keyword: Optional[str] = None):
        """
        Fetches all news data from Event Registry API, paginating through all results.

        Args:
            keyword (str, optional): Specific keyword to search for. Defaults to None.

        Returns:
            list: A list of news articles.
        """
        if app_settings.FETCH_STATIC_DATA:
            return random.sample(NEWS_STATIC_DATA.get("feed", []), 30)

        base_url = app_settings.NEWS_API_BASE_URL
        current_date = datetime.now(UTC).strftime("%Y-%m-%d")

        payload = {
            "apiKey": app_settings.NEWS_API_KEY,
            "dateStart": current_date,
            "articlesPage": 1,
        }

        if keyword:
            payload["keyword"] = [keyword]

        all_articles = []

        async with httpx.AsyncClient(timeout=15) as client:
            while True:
                response = await client.post(base_url, json=payload)
                response.raise_for_status()
                data: dict = response.json()
                articles = data.get("articles", {}).get("results", [])
                all_articles.extend(articles)

                # Check if we've reached the last page
                total_pages = data.get("articles", {}).get("pages", 1)
                if payload["articlesPage"] >= total_pages:
                    break

                payload["articlesPage"] += 1

        return all_articles

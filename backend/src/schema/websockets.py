from typing import List, Optional

from pydantic import BaseModel


class WebSocketMessage(BaseModel):
    title: str
    url: str
    time_published: str
    authors: List[str]
    summary: str
    banner_image: Optional[str]
    source: str
    overall_sentiment_score: float
    overall_sentiment_label: str
    deep_analysis: Optional[str] = None

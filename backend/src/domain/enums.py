from enum import Enum


class ContentTone(str, Enum):
    FORMAL = "Formal"
    NEUTRAL = "Neutral"
    INFORMAL = "Informal"


class PostStatus(str, Enum):
    DRAFT = "Draft"
    APPROVED = "Approved"
    PUBLISHED = "Published"


class MarketEventSource(str, Enum):
    ALPHA_VANTAGE_API = "Alpha Vantage"
    EVENT_REGISTRY_API = "Event Registry"
    CUSTOM_EVENT = "Custom Event"


class SentimentalAnalysis(str, Enum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"


class PriorityFlag(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class MarketEvenProcessingtStatus(str, Enum):
    RESEARCHING = "Researching"
    WRITING = "Writing"
    FETCHING_ANALYTICS = "Fetching Analytics"
    DRAFTED = "Drafted"
    FAILED = "Failed"

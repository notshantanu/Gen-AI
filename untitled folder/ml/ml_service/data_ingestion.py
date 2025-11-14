"""
Data ingestion module for social media signals.
Mock implementations for Twitter/X and YouTube data.
"""
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/aurapoints")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def fetch_twitter_data(twitter_handle: str) -> Dict:
    """
    Mock Twitter/X data fetcher.
    In production, this would use Twitter API v2.
    """
    # Mock data structure
    return {
        "handle": twitter_handle,
        "followers": random.randint(10000, 10000000),
        "tweets_last_24h": random.randint(0, 50),
        "likes_last_24h": random.randint(0, 10000),
        "retweets_last_24h": random.randint(0, 5000),
        "mentions_last_24h": random.randint(0, 1000),
        "sentiment_score": random.uniform(-1, 1),  # Mock sentiment
        "timestamp": datetime.utcnow().isoformat()
    }


def fetch_youtube_data(channel_id: str) -> Dict:
    """
    Mock YouTube data fetcher.
    In production, this would use YouTube Data API v3.
    """
    # Mock data structure
    return {
        "channel_id": channel_id,
        "subscribers": random.randint(10000, 5000000),
        "videos_last_24h": random.randint(0, 5),
        "views_last_24h": random.randint(0, 1000000),
        "likes_last_24h": random.randint(0, 50000),
        "comments_last_24h": random.randint(0, 10000),
        "sentiment_score": random.uniform(-1, 1),  # Mock sentiment
        "timestamp": datetime.utcnow().isoformat()
    }


def store_raw_signal(
    personality_id: int,
    source: str,
    raw_data: Dict,
    db_session
):
    """Store raw ML signal data in database."""
    from ml_service.models import MLSignalRaw
    
    signal = MLSignalRaw(
        personality_id=personality_id,
        source=source,
        raw_data=raw_data
    )
    db_session.add(signal)
    db_session.commit()
    return signal


def ingest_personality_data(personality_id: int, twitter_handle: Optional[str], youtube_channel_id: Optional[str]):
    """
    Ingest data for a personality from all available sources.
    """
    db = SessionLocal()
    try:
        signals = []
        
        if twitter_handle:
            twitter_data = fetch_twitter_data(twitter_handle)
            signal = store_raw_signal(personality_id, "twitter", twitter_data, db)
            signals.append(signal)
        
        if youtube_channel_id:
            youtube_data = fetch_youtube_data(youtube_channel_id)
            signal = store_raw_signal(personality_id, "youtube", youtube_data, db)
            signals.append(signal)
        
        return signals
    finally:
        db.close()


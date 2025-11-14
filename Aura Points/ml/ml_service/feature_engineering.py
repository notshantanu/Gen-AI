"""
Feature engineering module for ML predictions.
Extracts features from raw social media data.
"""
from typing import Dict, List, Optional
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ml_service.models import MLSignalRaw


def calculate_sentiment_score(raw_data: Dict) -> Decimal:
    """
    Calculate sentiment score from raw data.
    For MVP, uses mock sentiment from raw_data.
    In production, would use NLP models (VADER, TextBlob, etc.)
    """
    # Mock: extract sentiment from raw_data if available
    if "sentiment_score" in raw_data:
        return Decimal(str(raw_data["sentiment_score"]))
    
    # Default neutral
    return Decimal("0.0")


def calculate_engagement_delta(
    current_data: Dict,
    previous_data: Optional[Dict],
    source: str
) -> Decimal:
    """
    Calculate engagement delta (change in engagement metrics).
    """
    if not previous_data:
        return Decimal("0.0")
    
    if source == "twitter":
        current_engagement = (
            current_data.get("likes_last_24h", 0) +
            current_data.get("retweets_last_24h", 0) * 2 +
            current_data.get("mentions_last_24h", 0)
        )
        previous_engagement = (
            previous_data.get("likes_last_24h", 0) +
            previous_data.get("retweets_last_24h", 0) * 2 +
            previous_data.get("mentions_last_24h", 0)
        )
    elif source == "youtube":
        current_engagement = (
            current_data.get("views_last_24h", 0) +
            current_data.get("likes_last_24h", 0) * 2 +
            current_data.get("comments_last_24h", 0) * 3
        )
        previous_engagement = (
            previous_data.get("views_last_24h", 0) +
            previous_data.get("likes_last_24h", 0) * 2 +
            previous_data.get("comments_last_24h", 0) * 3
        )
    else:
        return Decimal("0.0")
    
    delta = current_engagement - previous_engagement
    # Normalize by previous engagement to get percentage change
    if previous_engagement > 0:
        return Decimal(str(delta / previous_engagement))
    return Decimal("0.0")


def calculate_volume_velocity(
    current_data: Dict,
    source: str
) -> Decimal:
    """
    Calculate volume velocity (rate of content production).
    """
    if source == "twitter":
        velocity = current_data.get("tweets_last_24h", 0)
    elif source == "youtube":
        velocity = current_data.get("videos_last_24h", 0) * 10  # Videos weighted more
    else:
        return Decimal("0.0")
    
    return Decimal(str(velocity))


def extract_features(
    signal: MLSignalRaw,
    db_session: Session
) -> Dict:
    """
    Extract all features from a raw signal.
    """
    raw_data = signal.raw_data
    
    # Calculate sentiment
    sentiment_score = calculate_sentiment_score(raw_data)
    
    # Get previous signal for delta calculation
    previous_signal = db_session.query(MLSignalRaw).filter(
        MLSignalRaw.personality_id == signal.personality_id,
        MLSignalRaw.source == signal.source,
        MLSignalRaw.id < signal.id
    ).order_by(MLSignalRaw.timestamp.desc()).first()
    
    previous_data = previous_signal.raw_data if previous_signal else None
    engagement_delta = calculate_engagement_delta(raw_data, previous_data, signal.source)
    volume_velocity = calculate_volume_velocity(raw_data, signal.source)
    
    features = {
        "sentiment_score": float(sentiment_score),
        "engagement_delta": float(engagement_delta),
        "volume_velocity": float(volume_velocity),
        "source": signal.source
    }
    
    # Update signal with processed features
    signal.sentiment_score = sentiment_score
    signal.engagement_delta = engagement_delta
    signal.volume_velocity = volume_velocity
    signal.processed_features = features
    
    db_session.commit()
    
    return features


def aggregate_features_for_personality(
    personality_id: int,
    db_session: Session
) -> Dict:
    """
    Aggregate features from all sources for a personality.
    """
    # Get latest signals for each source
    signals = db_session.query(MLSignalRaw).filter(
        MLSignalRaw.personality_id == personality_id
    ).order_by(MLSignalRaw.timestamp.desc()).all()
    
    if not signals:
        return {
            "sentiment_score": 0.0,
            "engagement_delta": 0.0,
            "volume_velocity": 0.0
        }
    
    # Aggregate by source (weighted average)
    twitter_features = [s for s in signals if s.source == "twitter"][:1]
    youtube_features = [s for s in signals if s.source == "youtube"][:1]
    
    all_features = []
    if twitter_features:
        all_features.append(twitter_features[0].processed_features or {})
    if youtube_features:
        all_features.append(youtube_features[0].processed_features or {})
    
    if not all_features:
        return {
            "sentiment_score": 0.0,
            "engagement_delta": 0.0,
            "volume_velocity": 0.0
        }
    
    # Average the features
    aggregated = {
        "sentiment_score": sum(f.get("sentiment_score", 0) for f in all_features) / len(all_features),
        "engagement_delta": sum(f.get("engagement_delta", 0) for f in all_features) / len(all_features),
        "volume_velocity": sum(f.get("volume_velocity", 0) for f in all_features) / len(all_features)
    }
    
    return aggregated


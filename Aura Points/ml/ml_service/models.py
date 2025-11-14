"""
Database models for ML service (mirrors backend models).
"""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MLSignalRaw(Base):
    """Raw ML signals from social media data."""
    __tablename__ = "ml_signals_raw"
    
    id = Column(Integer, primary_key=True, index=True)
    personality_id = Column(Integer, ForeignKey("personalities.id"), nullable=False)
    source = Column(String(50), nullable=False)
    raw_data = Column(JSON, nullable=False)
    processed_features = Column(JSON, nullable=True)
    sentiment_score = Column(Numeric(5, 4), nullable=True)
    engagement_delta = Column(Numeric(20, 8), nullable=True)
    volume_velocity = Column(Numeric(20, 8), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


"""
SQLAlchemy models for Aura Points platform.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Numeric, DateTime, ForeignKey, 
    Boolean, JSON, Text, Index
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User accounts for the platform."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    wallet_address = Column(String(42), unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trades = relationship("Trade", back_populates="user")
    parlays = relationship("Parlay", back_populates="user")


class Personality(Base):
    """Real-world personalities that users can trade."""
    __tablename__ = "personalities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    twitter_handle = Column(String(100), nullable=True)
    youtube_channel_id = Column(String(100), nullable=True)
    image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    aura_scores = relationship("AuraScore", back_populates="personality")
    aura_score_history = relationship("AuraScoreHistory", back_populates="personality")
    trades = relationship("Trade", back_populates="personality")
    ml_signals = relationship("MLSignalRaw", back_populates="personality")
    
    __table_args__ = (
        Index('idx_personality_slug', 'slug'),
    )


class AuraScore(Base):
    """Current aura score for each personality."""
    __tablename__ = "aura_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    personality_id = Column(Integer, ForeignKey("personalities.id"), nullable=False, unique=True)
    current_score = Column(Numeric(20, 8), nullable=False, default=Decimal("100.0"))
    momentum_score = Column(Numeric(10, 4), nullable=True)  # ML prediction
    price_per_share = Column(Numeric(20, 8), nullable=False)  # Calculated from score
    total_shares = Column(Numeric(20, 8), nullable=False, default=Decimal("0"))
    volume_24h = Column(Numeric(20, 8), nullable=False, default=Decimal("0"))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    personality = relationship("Personality", back_populates="aura_scores")
    
    __table_args__ = (
        Index('idx_aura_score_personality', 'personality_id'),
        Index('idx_aura_score_updated', 'updated_at'),
    )


class AuraScoreHistory(Base):
    """Historical aura score snapshots."""
    __tablename__ = "aura_score_history"
    
    id = Column(Integer, primary_key=True, index=True)
    personality_id = Column(Integer, ForeignKey("personalities.id"), nullable=False)
    score = Column(Numeric(20, 8), nullable=False)
    momentum_score = Column(Numeric(10, 4), nullable=True)
    price_per_share = Column(Numeric(20, 8), nullable=False)
    volume_24h = Column(Numeric(20, 8), nullable=False, default=Decimal("0"))
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    personality = relationship("Personality", back_populates="aura_score_history")
    
    __table_args__ = (
        Index('idx_history_personality_timestamp', 'personality_id', 'timestamp'),
    )


class Trade(Base):
    """Trade records for aura point transactions."""
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    personality_id = Column(Integer, ForeignKey("personalities.id"), nullable=False)
    trade_type = Column(String(10), nullable=False)  # 'buy' or 'sell'
    shares = Column(Numeric(20, 8), nullable=False)
    price_per_share = Column(Numeric(20, 8), nullable=False)
    total_cost = Column(Numeric(20, 8), nullable=False)  # shares * price
    transaction_hash = Column(String(66), unique=True, nullable=True)  # Blockchain tx hash
    status = Column(String(20), default="pending")  # pending, confirmed, failed
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = relationship("User", back_populates="trades")
    personality = relationship("Personality", back_populates="trades")
    
    __table_args__ = (
        Index('idx_trade_user', 'user_id'),
        Index('idx_trade_personality', 'personality_id'),
        Index('idx_trade_created', 'created_at'),
    )


class Parlay(Base):
    """Multi-leg speculative bundles."""
    __tablename__ = "parlays"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    legs = Column(JSON, nullable=False)  # [{"personality_id": 1, "direction": "up", "threshold": 110}]
    total_stake = Column(Numeric(20, 8), nullable=False)
    potential_payout = Column(Numeric(20, 8), nullable=False)
    status = Column(String(20), default="pending")  # pending, active, won, lost, cancelled
    contract_address = Column(String(42), nullable=True)  # Blockchain contract address
    transaction_hash = Column(String(66), nullable=True)
    resolution_data = Column(JSON, nullable=True)  # Results when resolved
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    resolved_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="parlays")
    
    __table_args__ = (
        Index('idx_parlay_user', 'user_id'),
        Index('idx_parlay_status', 'status'),
    )


class MLSignalRaw(Base):
    """Raw ML signals from social media data."""
    __tablename__ = "ml_signals_raw"
    
    id = Column(Integer, primary_key=True, index=True)
    personality_id = Column(Integer, ForeignKey("personalities.id"), nullable=False)
    source = Column(String(50), nullable=False)  # 'twitter', 'youtube'
    raw_data = Column(JSON, nullable=False)  # Raw API response
    processed_features = Column(JSON, nullable=True)  # Extracted features
    sentiment_score = Column(Numeric(5, 4), nullable=True)  # -1 to 1
    engagement_delta = Column(Numeric(20, 8), nullable=True)
    volume_velocity = Column(Numeric(20, 8), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    personality = relationship("Personality", back_populates="ml_signals")
    
    __table_args__ = (
        Index('idx_ml_signal_personality', 'personality_id'),
        Index('idx_ml_signal_timestamp', 'timestamp'),
        Index('idx_ml_signal_source', 'source'),
    )


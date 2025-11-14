"""
Pydantic schemas for request/response validation.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field


# Auth Schemas
class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)
    wallet_address: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    wallet_address: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Personality Schemas
class PersonalityBase(BaseModel):
    name: str
    description: Optional[str] = None
    twitter_handle: Optional[str] = None
    youtube_channel_id: Optional[str] = None
    image_url: Optional[str] = None


class PersonalityCreate(PersonalityBase):
    pass


class PersonalityResponse(PersonalityBase):
    id: int
    slug: str
    is_active: bool
    created_at: datetime
    current_score: Optional[Decimal] = None
    momentum_score: Optional[Decimal] = None
    price_per_share: Optional[Decimal] = None

    class Config:
        from_attributes = True


class AuraScoreHistoryResponse(BaseModel):
    id: int
    personality_id: int
    score: Decimal
    momentum_score: Optional[Decimal]
    price_per_share: Decimal
    volume_24h: Decimal
    timestamp: datetime

    class Config:
        from_attributes = True


# Trade Schemas
class TradeCreate(BaseModel):
    personality_id: int
    trade_type: str = Field(..., pattern="^(buy|sell)$")
    shares: Decimal = Field(..., gt=0)
    transaction_hash: Optional[str] = None


class TradeResponse(BaseModel):
    id: int
    user_id: int
    personality_id: int
    trade_type: str
    shares: Decimal
    price_per_share: Decimal
    total_cost: Decimal
    transaction_hash: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# Parlay Schemas
class ParlayLeg(BaseModel):
    personality_id: int
    direction: str = Field(..., pattern="^(up|down)$")
    threshold: Decimal = Field(..., gt=0)


class ParlayCreate(BaseModel):
    name: str
    description: Optional[str] = None
    legs: List[ParlayLeg] = Field(..., min_items=2)
    total_stake: Decimal = Field(..., gt=0)
    transaction_hash: Optional[str] = None


class ParlayResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str]
    legs: List[Dict[str, Any]]
    total_stake: Decimal
    potential_payout: Decimal
    status: str
    contract_address: Optional[str]
    transaction_hash: Optional[str]
    resolution_data: Optional[Dict[str, Any]]
    created_at: datetime
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True


# ML Schemas
class MLSignalResponse(BaseModel):
    personality_id: int
    personality_name: str
    momentum_score: Decimal
    sentiment_score: Optional[Decimal]
    engagement_delta: Optional[Decimal]
    volume_velocity: Optional[Decimal]
    updated_at: datetime


class TopGainersResponse(BaseModel):
    personalities: List[MLSignalResponse]


class TopLosersResponse(BaseModel):
    personalities: List[MLSignalResponse]


"""
ML and signals routes.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Personality, AuraScore, MLSignalRaw
from schemas import MLSignalResponse, TopGainersResponse, TopLosersResponse
from auth import get_current_active_user, get_current_admin_user
from pricing import update_aura_score
from datetime import datetime, timedelta

router = APIRouter(prefix="/ml", tags=["ml"])


@router.post("/refresh")
def refresh_aura_scores(
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Admin endpoint to trigger ML refresh and aura score updates."""
    # This would typically call the ML service
    # For MVP, we'll return a success message
    return {
        "message": "ML refresh triggered",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/signals/top-gainers", response_model=TopGainersResponse)
def get_top_gainers(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get personalities with highest momentum scores."""
    # Get personalities with highest momentum scores
    aura_scores = db.query(AuraScore, Personality).join(
        Personality, AuraScore.personality_id == Personality.id
    ).filter(
        Personality.is_active == True,
        AuraScore.momentum_score.isnot(None)
    ).order_by(
        AuraScore.momentum_score.desc()
    ).limit(limit).all()
    
    personalities = []
    for aura_score, personality in aura_scores:
        # Get latest ML signal
        latest_signal = db.query(MLSignalRaw).filter(
            MLSignalRaw.personality_id == personality.id
        ).order_by(MLSignalRaw.timestamp.desc()).first()
        
        personalities.append(MLSignalResponse(
            personality_id=personality.id,
            personality_name=personality.name,
            momentum_score=aura_score.momentum_score or 0,
            sentiment_score=latest_signal.sentiment_score if latest_signal else None,
            engagement_delta=latest_signal.engagement_delta if latest_signal else None,
            volume_velocity=latest_signal.volume_velocity if latest_signal else None,
            updated_at=aura_score.updated_at
        ))
    
    return TopGainersResponse(personalities=personalities)


@router.get("/signals/top-losers", response_model=TopLosersResponse)
def get_top_losers(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get personalities with lowest momentum scores."""
    # Get personalities with lowest momentum scores
    aura_scores = db.query(AuraScore, Personality).join(
        Personality, AuraScore.personality_id == Personality.id
    ).filter(
        Personality.is_active == True,
        AuraScore.momentum_score.isnot(None)
    ).order_by(
        AuraScore.momentum_score.asc()
    ).limit(limit).all()
    
    personalities = []
    for aura_score, personality in aura_scores:
        # Get latest ML signal
        latest_signal = db.query(MLSignalRaw).filter(
            MLSignalRaw.personality_id == personality.id
        ).order_by(MLSignalRaw.timestamp.desc()).first()
        
        personalities.append(MLSignalResponse(
            personality_id=personality.id,
            personality_name=personality.name,
            momentum_score=aura_score.momentum_score or 0,
            sentiment_score=latest_signal.sentiment_score if latest_signal else None,
            engagement_delta=latest_signal.engagement_delta if latest_signal else None,
            volume_velocity=latest_signal.volume_velocity if latest_signal else None,
            updated_at=aura_score.updated_at
        ))
    
    return TopLosersResponse(personalities=personalities)


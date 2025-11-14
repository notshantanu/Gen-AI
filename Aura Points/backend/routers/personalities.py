"""
Personality routes.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from database import get_db
from models import Personality, AuraScore, AuraScoreHistory
from schemas import PersonalityResponse, AuraScoreHistoryResponse
from auth import get_current_active_user
from pricing import get_or_create_aura_score

router = APIRouter(prefix="/personalities", tags=["personalities"])


@router.get("", response_model=List[PersonalityResponse])
def list_personalities(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all active personalities."""
    personalities = db.query(Personality).filter(
        Personality.is_active == True
    ).offset(skip).limit(limit).all()
    
    result = []
    for p in personalities:
        aura_score = get_or_create_aura_score(db, p.id)
        result.append({
            **p.__dict__,
            "current_score": aura_score.current_score,
            "momentum_score": aura_score.momentum_score,
            "price_per_share": aura_score.price_per_share
        })
    
    return result


@router.get("/{personality_id}", response_model=PersonalityResponse)
def get_personality(personality_id: int, db: Session = Depends(get_db)):
    """Get a specific personality by ID."""
    personality = db.query(Personality).filter(
        Personality.id == personality_id,
        Personality.is_active == True
    ).first()
    
    if not personality:
        raise HTTPException(status_code=404, detail="Personality not found")
    
    aura_score = get_or_create_aura_score(db, personality_id)
    return {
        **personality.__dict__,
        "current_score": aura_score.current_score,
        "momentum_score": aura_score.momentum_score,
        "price_per_share": aura_score.price_per_share
    }


@router.get("/{personality_id}/history", response_model=List[AuraScoreHistoryResponse])
def get_personality_history(
    personality_id: int,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get historical aura score data for a personality."""
    personality = db.query(Personality).filter(
        Personality.id == personality_id
    ).first()
    
    if not personality:
        raise HTTPException(status_code=404, detail="Personality not found")
    
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    history = db.query(AuraScoreHistory).filter(
        AuraScoreHistory.personality_id == personality_id,
        AuraScoreHistory.timestamp >= cutoff_date
    ).order_by(AuraScoreHistory.timestamp.desc()).all()
    
    return history


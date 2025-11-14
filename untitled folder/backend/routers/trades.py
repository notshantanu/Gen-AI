"""
Trading routes.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal
from database import get_db
from models import Trade, Personality, AuraScore
from schemas import TradeCreate, TradeResponse
from auth import get_current_active_user
from pricing import get_or_create_aura_score

router = APIRouter(prefix="/trades", tags=["trades"])


@router.post("/buy", response_model=TradeResponse, status_code=201)
def buy_shares(
    trade_data: TradeCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Buy aura shares for a personality."""
    if trade_data.trade_type != "buy":
        raise HTTPException(status_code=400, detail="Use /trades/sell for sell orders")
    
    # Get personality and aura score
    personality = db.query(Personality).filter(
        Personality.id == trade_data.personality_id,
        Personality.is_active == True
    ).first()
    
    if not personality:
        raise HTTPException(status_code=404, detail="Personality not found")
    
    aura_score = get_or_create_aura_score(db, trade_data.personality_id)
    
    # Calculate total cost
    total_cost = trade_data.shares * aura_score.price_per_share
    
    # Create trade record
    trade = Trade(
        user_id=current_user.id,
        personality_id=trade_data.personality_id,
        trade_type="buy",
        shares=trade_data.shares,
        price_per_share=aura_score.price_per_share,
        total_cost=total_cost,
        transaction_hash=trade_data.transaction_hash,
        status="pending" if not trade_data.transaction_hash else "confirmed"
    )
    
    # Update aura score (buying increases total shares)
    aura_score.total_shares += trade_data.shares
    aura_score.volume_24h += total_cost
    
    db.add(trade)
    db.commit()
    db.refresh(trade)
    
    return trade


@router.post("/sell", response_model=TradeResponse, status_code=201)
def sell_shares(
    trade_data: TradeCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Sell aura shares for a personality."""
    if trade_data.trade_type != "sell":
        raise HTTPException(status_code=400, detail="Use /trades/buy for buy orders")
    
    # Get personality and aura score
    personality = db.query(Personality).filter(
        Personality.id == trade_data.personality_id,
        Personality.is_active == True
    ).first()
    
    if not personality:
        raise HTTPException(status_code=404, detail="Personality not found")
    
    aura_score = get_or_create_aura_score(db, trade_data.personality_id)
    
    # Check user's holdings (simplified - in production, track per-user balances)
    # For MVP, we'll allow selling if total shares exist
    if aura_score.total_shares < trade_data.shares:
        raise HTTPException(status_code=400, detail="Insufficient shares available")
    
    # Calculate total cost
    total_cost = trade_data.shares * aura_score.price_per_share
    
    # Create trade record
    trade = Trade(
        user_id=current_user.id,
        personality_id=trade_data.personality_id,
        trade_type="sell",
        shares=trade_data.shares,
        price_per_share=aura_score.price_per_share,
        total_cost=total_cost,
        transaction_hash=trade_data.transaction_hash,
        status="pending" if not trade_data.transaction_hash else "confirmed"
    )
    
    # Update aura score (selling decreases total shares)
    aura_score.total_shares -= trade_data.shares
    aura_score.volume_24h += total_cost
    
    db.add(trade)
    db.commit()
    db.refresh(trade)
    
    return trade


@router.get("/my", response_model=List[TradeResponse])
def get_my_trades(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's trade history."""
    trades = db.query(Trade).filter(
        Trade.user_id == current_user.id
    ).order_by(Trade.created_at.desc()).offset(skip).limit(limit).all()
    
    return trades


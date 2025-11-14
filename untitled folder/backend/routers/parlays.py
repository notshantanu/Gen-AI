"""
Parlay routes.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal
from database import get_db
from models import Parlay
from schemas import ParlayCreate, ParlayResponse
from auth import get_current_active_user

router = APIRouter(prefix="/parlays", tags=["parlays"])


def calculate_potential_payout(stake: Decimal, num_legs: int) -> Decimal:
    """Calculate potential payout based on stake and number of legs."""
    # Simple formula: payout = stake * (2 ^ num_legs)
    # More legs = higher risk = higher payout
    multiplier = Decimal("2") ** num_legs
    return stake * multiplier


@router.post("", response_model=ParlayResponse, status_code=201)
def create_parlay(
    parlay_data: ParlayCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new parlay."""
    if len(parlay_data.legs) < 2:
        raise HTTPException(status_code=400, detail="Parlay must have at least 2 legs")
    
    # Calculate potential payout
    potential_payout = calculate_potential_payout(
        parlay_data.total_stake,
        len(parlay_data.legs)
    )
    
    # Convert legs to JSON-serializable format
    legs_json = [leg.dict() for leg in parlay_data.legs]
    
    parlay = Parlay(
        user_id=current_user.id,
        name=parlay_data.name,
        description=parlay_data.description,
        legs=legs_json,
        total_stake=parlay_data.total_stake,
        potential_payout=potential_payout,
        transaction_hash=parlay_data.transaction_hash,
        status="pending" if not parlay_data.transaction_hash else "active"
    )
    
    db.add(parlay)
    db.commit()
    db.refresh(parlay)
    
    return parlay


@router.get("", response_model=List[ParlayResponse])
def list_parlays(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all parlays."""
    parlays = db.query(Parlay).order_by(
        Parlay.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return parlays


@router.get("/{parlay_id}", response_model=ParlayResponse)
def get_parlay(parlay_id: int, db: Session = Depends(get_db)):
    """Get a specific parlay by ID."""
    parlay = db.query(Parlay).filter(Parlay.id == parlay_id).first()
    
    if not parlay:
        raise HTTPException(status_code=404, detail="Parlay not found")
    
    return parlay


@router.get("/my", response_model=List[ParlayResponse])
def get_my_parlays(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's parlays."""
    parlays = db.query(Parlay).filter(
        Parlay.user_id == current_user.id
    ).order_by(Parlay.created_at.desc()).offset(skip).limit(limit).all()
    
    return parlays


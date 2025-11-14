"""
Pricing logic for aura points.
Deterministic formula: price = base_price * (1 + score_multiplier * (current_score / base_score - 1))
"""
from decimal import Decimal
from typing import Optional
from sqlalchemy.orm import Session
from models import AuraScore, Personality

BASE_SCORE = Decimal("100.0")
BASE_PRICE = Decimal("1.0")  # 1 AURA token per share at base score
SCORE_MULTIPLIER = Decimal("0.5")  # Price sensitivity to score changes


def calculate_price_per_share(current_score: Decimal) -> Decimal:
    """
    Calculate price per share based on current aura score.
    Formula: price = base_price * (1 + score_multiplier * (current_score / base_score - 1))
    """
    if current_score <= 0:
        return BASE_PRICE
    
    score_ratio = current_score / BASE_SCORE
    price = BASE_PRICE * (Decimal("1") + SCORE_MULTIPLIER * (score_ratio - Decimal("1")))
    return max(price, Decimal("0.01"))  # Minimum price floor


def get_or_create_aura_score(db: Session, personality_id: int) -> AuraScore:
    """Get or create aura score for a personality."""
    aura_score = db.query(AuraScore).filter(
        AuraScore.personality_id == personality_id
    ).first()
    
    if not aura_score:
        aura_score = AuraScore(
            personality_id=personality_id,
            current_score=BASE_SCORE,
            price_per_share=calculate_price_per_share(BASE_SCORE),
            total_shares=Decimal("0")
        )
        db.add(aura_score)
        db.commit()
        db.refresh(aura_score)
    
    return aura_score


def update_aura_score(
    db: Session,
    personality_id: int,
    new_score: Decimal,
    momentum_score: Optional[Decimal] = None
) -> AuraScore:
    """Update aura score and recalculate price."""
    aura_score = get_or_create_aura_score(db, personality_id)
    
    old_score = aura_score.current_score
    aura_score.current_score = new_score
    aura_score.momentum_score = momentum_score
    aura_score.price_per_share = calculate_price_per_share(new_score)
    
    # Create history entry
    from models import AuraScoreHistory
    history = AuraScoreHistory(
        personality_id=personality_id,
        score=new_score,
        momentum_score=momentum_score,
        price_per_share=aura_score.price_per_share,
        volume_24h=aura_score.volume_24h
    )
    db.add(history)
    db.commit()
    db.refresh(aura_score)
    
    return aura_score


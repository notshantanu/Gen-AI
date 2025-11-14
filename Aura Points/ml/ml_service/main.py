"""
Main ML service application.
Handles data ingestion, feature engineering, and momentum prediction.
"""
import os
import time
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from ml_service.data_ingestion import ingest_personality_data
from ml_service.feature_engineering import extract_features, aggregate_features_for_personality
from ml_service.model import predict_momentum, train_model, get_predictor
from ml_service.models import MLSignalRaw, Base

# Import backend models for AuraScore
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))
from models import Personality, AuraScore

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/aurapoints")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def update_aura_scores():
    """
    Main function to update aura scores for all personalities.
    Runs data ingestion, feature engineering, and prediction.
    """
    db = SessionLocal()
    try:
        # Get all active personalities
        personalities = db.query(Personality).filter(
            Personality.is_active == True
        ).all()
        
        print(f"Processing {len(personalities)} personalities...")
        
        for personality in personalities:
            try:
                # 1. Ingest data
                print(f"Ingesting data for {personality.name}...")
                signals = ingest_personality_data(
                    personality.id,
                    personality.twitter_handle,
                    personality.youtube_channel_id
                )
                
                # 2. Extract features from latest signals
                for signal in signals:
                    extract_features(signal, db)
                
                # 3. Aggregate features
                features = aggregate_features_for_personality(personality.id, db)
                
                # 4. Predict momentum
                momentum_score = predict_momentum(personality.id, features)
                
                # 5. Update aura score
                # Calculate new score based on momentum
                # Simple formula: new_score = current_score * (1 + momentum_score * 0.1)
                aura_score = db.query(AuraScore).filter(
                    AuraScore.personality_id == personality.id
                ).first()
                
                if aura_score:
                    from decimal import Decimal
                    current_score = float(aura_score.current_score)
                    new_score = current_score * (1 + momentum_score * 0.1)
                    new_score = max(new_score, 1.0)  # Minimum score of 1.0
                    
                    # Update in database
                    # Import pricing function directly
                    import sys
                    import os
                    backend_path = os.path.join(os.path.dirname(__file__), '../../backend')
                    if backend_path not in sys.path:
                        sys.path.insert(0, backend_path)
                    from pricing import update_aura_score
                    update_aura_score(db, personality.id, Decimal(str(new_score)), Decimal(str(momentum_score)))
                    
                    print(f"Updated {personality.name}: score={new_score:.2f}, momentum={momentum_score:.4f}")
                else:
                    print(f"No aura score found for {personality.name}")
                
            except Exception as e:
                print(f"Error processing {personality.name}: {e}")
                continue
        
        print("Aura score update complete!")
        
    finally:
        db.close()


def run_scheduled_updates(interval_minutes: int = 60):
    """
    Run scheduled updates at specified interval.
    """
    print(f"Starting scheduled ML updates (interval: {interval_minutes} minutes)")
    
    # Train model on startup
    print("Training model...")
    train_model()
    
    while True:
        try:
            update_aura_scores()
        except Exception as e:
            print(f"Error in scheduled update: {e}")
        
        print(f"Sleeping for {interval_minutes} minutes...")
        time.sleep(interval_minutes * 60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "train":
        # Train model only
        print("Training model...")
        train_model()
    elif len(sys.argv) > 1 and sys.argv[1] == "update":
        # Single update
        update_aura_scores()
    else:
        # Run scheduled updates
        run_scheduled_updates(interval_minutes=60)


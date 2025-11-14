"""
ML model for momentum prediction.
Uses Gradient Boosting Trees (XGBoost-like approach with sklearn).
"""
import os
import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from typing import Dict, Optional
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/aurapoints")
MODEL_PATH = os.getenv("MODEL_PATH", "./models/momentum_model.pkl")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class MomentumPredictor:
    """Momentum prediction model."""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or MODEL_PATH
        self.model = None
        self.feature_names = ["sentiment_score", "engagement_delta", "volume_velocity"]
        
        # Create models directory if it doesn't exist
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        # Load existing model if available
        if os.path.exists(self.model_path):
            self.load_model()
        else:
            # Initialize with default model
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
    
    def load_model(self):
        """Load trained model from disk."""
        self.model = joblib.load(self.model_path)
    
    def save_model(self):
        """Save trained model to disk."""
        joblib.dump(self.model, self.model_path)
    
    def prepare_features(self, features: Dict) -> np.ndarray:
        """Prepare features for prediction."""
        feature_vector = np.array([
            features.get("sentiment_score", 0.0),
            features.get("engagement_delta", 0.0),
            features.get("volume_velocity", 0.0)
        ]).reshape(1, -1)
        return feature_vector
    
    def predict(self, features: Dict) -> float:
        """
        Predict momentum score for given features.
        Returns a score between -1 and 1 (negative = downward momentum, positive = upward).
        """
        if self.model is None:
            # Return default prediction if model not trained
            return 0.0
        
        feature_vector = self.prepare_features(features)
        prediction = self.model.predict(feature_vector)[0]
        
        # Clamp prediction to [-1, 1] range
        return np.clip(prediction, -1.0, 1.0)
    
    def train(self, X: np.ndarray, y: np.ndarray):
        """
        Train the model on provided data.
        X: feature matrix (n_samples, n_features)
        y: target values (momentum scores)
        """
        if self.model is None:
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Model trained - MSE: {mse:.4f}, R2: {r2:.4f}")
        
        # Save model
        self.save_model()
        
        return mse, r2
    
    def generate_synthetic_training_data(self, n_samples: int = 1000) -> tuple:
        """
        Generate synthetic training data for MVP.
        In production, this would use historical data from the database.
        """
        np.random.seed(42)
        
        # Generate synthetic features
        X = np.random.randn(n_samples, 3)
        X[:, 0] = np.clip(X[:, 0], -1, 1)  # sentiment_score
        X[:, 1] = np.clip(X[:, 1] * 0.5, -2, 2)  # engagement_delta
        X[:, 2] = np.abs(X[:, 2]) * 10  # volume_velocity
        
        # Generate synthetic targets (momentum scores)
        # Simple formula: weighted combination of features
        y = (
            0.4 * X[:, 0] +  # sentiment
            0.4 * np.tanh(X[:, 1]) +  # engagement delta
            0.2 * np.tanh(X[:, 2] / 10)  # volume velocity
        ) + np.random.randn(n_samples) * 0.1  # Add noise
        
        y = np.clip(y, -1, 1)
        
        return X, y


# Global model instance
_predictor = None


def get_predictor() -> MomentumPredictor:
    """Get or create global predictor instance."""
    global _predictor
    if _predictor is None:
        _predictor = MomentumPredictor()
    return _predictor


def predict_momentum(personality_id: int, features: Dict) -> float:
    """
    Predict momentum score for a personality.
    """
    predictor = get_predictor()
    return predictor.predict(features)


def train_model():
    """
    Train the momentum prediction model.
    For MVP, uses synthetic data. In production, would use historical data.
    """
    predictor = get_predictor()
    X, y = predictor.generate_synthetic_training_data(n_samples=1000)
    mse, r2 = predictor.train(X, y)
    return mse, r2


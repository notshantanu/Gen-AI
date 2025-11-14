# ML Service

Machine learning service for Aura Points platform. Handles data ingestion, feature engineering, and momentum prediction.

## Features

- **Data Ingestion**: Mock Twitter/X and YouTube data collection
- **Feature Engineering**: Sentiment analysis, engagement deltas, volume velocity
- **Momentum Prediction**: Gradient Boosting Trees model for predicting personality momentum

## Setup

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Train Model
```bash
python -m ml_service.main train
```

### Single Update
```bash
python -m ml_service.main update
```

### Scheduled Updates
```bash
python -m ml_service.main
```

## Environment Variables

See `.env.example` for required environment variables.


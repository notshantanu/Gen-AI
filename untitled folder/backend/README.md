# Backend API

FastAPI backend for Aura Points platform.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
uvicorn main:app --reload
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### Auth
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get token
- `GET /auth/me` - Get current user info

### Personalities
- `GET /personalities` - List all personalities
- `GET /personalities/{id}` - Get personality details
- `GET /personalities/{id}/history` - Get score history

### Trades
- `POST /trades/buy` - Buy shares
- `POST /trades/sell` - Sell shares
- `GET /trades/my` - Get user's trades

### Parlays
- `GET /parlays` - List all parlays
- `POST /parlays` - Create parlay
- `GET /parlays/{id}` - Get parlay details
- `GET /parlays/my` - Get user's parlays

### ML
- `POST /ml/refresh` - Trigger ML refresh (admin)
- `GET /ml/signals/top-gainers` - Get top gainers
- `GET /ml/signals/top-losers` - Get top losers


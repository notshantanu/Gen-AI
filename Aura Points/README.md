# Aura Points Platform

A blockchain-based digital currency market where users buy/sell "aura points" tied to real-world personalities. Aura scores update based on market activity and machine-learning predictions from social media signals.

## Architecture

This is a modular monorepo with the following structure:

- `/frontend` - Next.js + Tailwind frontend
- `/backend` - FastAPI + SQLAlchemy + Alembic backend
- `/ml` - Python ML service for sentiment analysis and momentum prediction
- `/contracts` - Solidity smart contracts + Hardhat
- `/shared` - Shared utilities and types

## Tech Stack

- **Frontend**: Next.js 14, React, Tailwind CSS, React Query, Web3 (MetaMask/WalletConnect)
- **Backend**: FastAPI, SQLAlchemy, Alembic, PostgreSQL, JWT auth
- **ML**: Python, scikit-learn, pandas, numpy
- **Blockchain**: Solidity, Hardhat, TypeChain
- **Database**: PostgreSQL

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- PostgreSQL 14+
- Docker (optional)

### Environment Variables

Create `.env` files in each service directory:

#### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/aurapoints
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
WEB3_PROVIDER_URL=http://localhost:8545
CONTRACT_ADDRESSES={"AuraToken":"","AuraMarket":"","ParlayContract":""}
```

#### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CHAIN_ID=31337
NEXT_PUBLIC_CONTRACT_ADDRESSES={"AuraToken":"","AuraMarket":"","ParlayContract":""}
```

#### ML (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/aurapoints
MODEL_PATH=./models/momentum_model.pkl
```

### Installation

1. **Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

2. **Frontend**:
```bash
cd frontend
npm install
npm run dev
```

3. **ML Service**:
```bash
cd ml
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m ml_service.main
```

4. **Contracts**:
```bash
cd contracts
npm install
npx hardhat compile
npx hardhat test
npx hardhat node  # Local blockchain
npx hardhat run scripts/deploy.js --network localhost
```

### Docker (Optional)

```bash
docker-compose up -d
```

## Features

- **Personality Trading**: Buy/sell aura points for real-world personalities
- **ML-Powered Predictions**: Momentum scores based on social media signals
- **Parlays**: Multi-leg speculative bundles
- **Real-time Updates**: Aura scores update based on market activity and ML predictions
- **Wallet Integration**: MetaMask/WalletConnect support

## Project Structure

See individual README files in each directory for detailed documentation.

## License

MIT


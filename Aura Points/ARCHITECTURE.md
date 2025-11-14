# Architecture Overview

## System Architecture

The Aura Points platform is built as a modular monorepo with clear separation of concerns:

```
/
├── frontend/          # Next.js frontend application
├── backend/           # FastAPI backend API
├── ml/                # Python ML service
├── contracts/         # Solidity smart contracts
└── shared/            # Shared utilities (if needed)
```

## Component Details

### Frontend (Next.js)
- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS
- **State Management**: React Query for server state
- **Web3**: Wagmi + Web3Modal for wallet integration
- **Charts**: Recharts for data visualization

### Backend (FastAPI)
- **Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Database**: PostgreSQL
- **Auth**: JWT tokens
- **API**: RESTful endpoints

### ML Service (Python)
- **Framework**: Standalone Python service
- **ML Library**: scikit-learn (Gradient Boosting)
- **Data Processing**: pandas, numpy
- **Features**: Sentiment, engagement deltas, volume velocity

### Smart Contracts (Solidity)
- **Framework**: Hardhat
- **Language**: Solidity 0.8.20
- **Contracts**:
  - AuraToken (ERC-20)
  - AuraMarket (Trading)
  - ParlayContract (Parlays)

## Data Flow

### Trading Flow
1. User connects wallet in frontend
2. User initiates trade (buy/sell)
3. Frontend generates transaction data from contract
4. User signs transaction with wallet
5. Transaction sent to blockchain
6. Backend API records trade with transaction hash
7. Smart contract updates on-chain balances
8. Backend updates aura scores and pricing

### ML Update Flow
1. ML service runs on schedule (every hour)
2. Ingests social media data for each personality
3. Extracts features (sentiment, engagement, volume)
4. Predicts momentum score using trained model
5. Updates aura scores in database
6. Triggers price recalculation

### Parlay Flow
1. User creates parlay with multiple legs
2. Frontend generates parlay creation transaction
3. User signs and submits transaction
4. ParlayContract stores parlay on-chain
5. Backend records parlay in database
6. Admin/oracle resolves parlay based on outcomes
7. Winners receive payout from contract

## Pricing Formula

The pricing formula is deterministic and transparent:

```
price = BASE_PRICE * (1 + SCORE_MULTIPLIER * (current_score / BASE_SCORE - 1))
```

Where:
- `BASE_PRICE = 1.0 AURA` (1 token per share at base score)
- `BASE_SCORE = 100.0` (baseline aura score)
- `SCORE_MULTIPLIER = 0.5` (price sensitivity)

This ensures:
- Price increases as score increases
- Price decreases as score decreases
- Minimum price floor of 0.01 AURA

## Security Considerations

1. **Smart Contracts**:
   - Use OpenZeppelin contracts for security
   - Comprehensive test coverage
   - Access control for admin functions

2. **Backend**:
   - JWT authentication
   - Input validation with Pydantic
   - SQL injection prevention via SQLAlchemy
   - CORS configuration

3. **Frontend**:
   - Wallet signature verification
   - Secure token storage
   - Input sanitization

## Scalability

The architecture supports horizontal scaling:

- **Frontend**: Stateless, can be replicated
- **Backend**: Stateless API, can use load balancer
- **Database**: PostgreSQL with read replicas
- **ML Service**: Can run multiple instances
- **Blockchain**: Decentralized by nature

## Future Enhancements

1. Real-time updates via WebSockets
2. Advanced ML models (LSTM, Transformer)
3. Real social media API integration
4. Oracle service for parlay resolution
5. Mobile app (React Native)
6. Advanced analytics dashboard
7. Governance token and DAO


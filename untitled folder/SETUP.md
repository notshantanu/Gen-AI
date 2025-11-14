# Setup Guide

Complete setup instructions for the Aura Points platform.

## Prerequisites

- Node.js 18+
- Python 3.10+
- PostgreSQL 14+
- Docker (optional, for containerized setup)

## Quick Start with Docker

1. Clone the repository and navigate to the project directory

2. Start all services:
```bash
docker-compose up -d
```

3. Run database migrations:
```bash
docker-compose exec backend alembic upgrade head
```

4. Access the services:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Manual Setup

### 1. Database Setup

```bash
# Create PostgreSQL database
createdb aurapoints

# Or using psql:
psql -U postgres
CREATE DATABASE aurapoints;
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL and secrets

# Run migrations
alembic upgrade head

# Start server
uvicorn main:app --reload
```

### 3. ML Service Setup

```bash
cd ml
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database URL

# Train model (optional, will auto-train on first run)
python -m ml_service.main train

# Run ML service
python -m ml_service.main
```

### 4. Smart Contracts Setup

```bash
cd contracts
npm install

# Compile contracts
npm run compile

# Run tests
npm run test

# Start local Hardhat node (in one terminal)
npm run node

# Deploy contracts (in another terminal)
npm run deploy
```

### 5. Frontend Setup

```bash
cd frontend
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your API URL and contract addresses

# Start development server
npm run dev
```

## Initial Data

To seed the database with sample personalities, you can use the FastAPI admin endpoints or directly insert data into PostgreSQL.

Example SQL:
```sql
INSERT INTO personalities (name, slug, description, is_active, created_at, updated_at)
VALUES 
  ('Elon Musk', 'elon-musk', 'Tech entrepreneur and CEO', true, NOW(), NOW()),
  ('Taylor Swift', 'taylor-swift', 'Singer-songwriter', true, NOW(), NOW());
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/aurapoints
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
WEB3_PROVIDER_URL=http://localhost:8545
CONTRACT_ADDRESSES={"AuraToken":"","AuraMarket":"","ParlayContract":""}
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CHAIN_ID=31337
NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID=your-walletconnect-project-id
NEXT_PUBLIC_CONTRACT_ADDRESSES={"AuraToken":"","AuraMarket":"","ParlayContract":""}
```

### ML (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/aurapoints
MODEL_PATH=./models/momentum_model.pkl
```

## Testing

### Backend Tests
```bash
cd backend
pytest  # If you add tests
```

### Contract Tests
```bash
cd contracts
npm run test
```

### Frontend Tests
```bash
cd frontend
npm run test  # If you add tests
```

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env files
- Verify database exists and user has permissions

### Contract Deployment Issues
- Ensure Hardhat node is running
- Check network configuration in hardhat.config.js
- Verify contract addresses in environment variables

### Frontend Connection Issues
- Verify NEXT_PUBLIC_API_URL matches backend URL
- Check CORS settings in backend/main.py
- Ensure backend is running

## Production Deployment

For production deployment:

1. Use environment-specific configuration files
2. Set strong JWT_SECRET
3. Use production database (managed PostgreSQL service)
4. Deploy contracts to mainnet/testnet
5. Configure proper CORS origins
6. Set up SSL/TLS certificates
7. Use process managers (PM2, systemd) for services
8. Set up monitoring and logging


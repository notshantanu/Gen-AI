# Frontend

Next.js frontend for Aura Points platform.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
cp .env.example .env.local
# Edit .env.local with your configuration
```

3. Run development server:
```bash
npm run dev
```

Visit http://localhost:3000

## Build for Production

```bash
npm run build
npm start
```

## Features

- **Landing Page**: Welcome page with platform overview
- **Personality Directory**: Browse all available personalities
- **Personality Detail**: View details, charts, and trade
- **Dashboard**: View portfolio and momentum picks
- **Parlays**: Create and manage parlays
- **Wallet Integration**: MetaMask/WalletConnect support

## Tech Stack

- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- React Query
- Wagmi (Web3)
- Recharts


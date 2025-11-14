# Smart Contracts

Solidity smart contracts for Aura Points platform, built with Hardhat.

## Contracts

- **AuraToken**: ERC-20 token for the platform
- **AuraMarket**: Market contract for buying/selling aura shares
- **ParlayContract**: Contract for managing multi-leg parlays

## Setup

1. Install dependencies:
```bash
npm install
```

2. Compile contracts:
```bash
npm run compile
```

3. Run tests:
```bash
npm run test
```

## Deployment

1. Start local Hardhat node:
```bash
npm run node
```

2. In another terminal, deploy contracts:
```bash
npm run deploy
```

Deployment addresses will be saved to `deployment-addresses.json`.

## Testing

Run the test suite:
```bash
npm run test
```

## Network Configuration

The default network is Hardhat's local network (chain ID: 31337). To deploy to other networks, update `hardhat.config.js` and use the `--network` flag.


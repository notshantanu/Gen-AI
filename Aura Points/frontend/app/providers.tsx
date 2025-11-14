'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { WagmiProvider } from 'wagmi'
import { createConfig, http } from 'wagmi'
import { mainnet, hardhat } from 'wagmi/chains'
import { createWeb3Modal } from '@web3modal/wagmi/react'
import { walletConnect, injected } from 'wagmi/connectors'

const projectId = process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID || 'your-project-id'

const metadata = {
  name: 'Aura Points',
  description: 'Personality Trading Platform',
  url: 'https://aurapoints.com',
  icons: ['https://aurapoints.com/logo.png']
}

const chains = [hardhat, mainnet] as const

const config = createConfig({
  chains,
  connectors: [
    walletConnect({ projectId, metadata, showQrModal: true }),
    injected({ shimDisconnect: true }),
  ],
  transports: {
    [hardhat.id]: http('http://localhost:8545'),
    [mainnet.id]: http(),
  },
})

createWeb3Modal({
  wagmiConfig: config,
  projectId,
  enableAnalytics: false,
})

const queryClient = new QueryClient()

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <WagmiProvider config={config}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </WagmiProvider>
  )
}


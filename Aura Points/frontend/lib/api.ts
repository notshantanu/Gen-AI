import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export interface User {
  id: number
  email: string
  username: string
  wallet_address: string | null
  is_active: boolean
  created_at: string
}

export interface Personality {
  id: number
  name: string
  slug: string
  description: string | null
  twitter_handle: string | null
  youtube_channel_id: string | null
  image_url: string | null
  is_active: boolean
  created_at: string
  current_score?: number
  momentum_score?: number
  price_per_share?: number
}

export interface Trade {
  id: number
  user_id: number
  personality_id: number
  trade_type: 'buy' | 'sell'
  shares: number
  price_per_share: number
  total_cost: number
  transaction_hash: string | null
  status: string
  created_at: string
}

export interface Parlay {
  id: number
  user_id: number
  name: string
  description: string | null
  legs: Array<{
    personality_id: number
    direction: 'up' | 'down'
    threshold: number
  }>
  total_stake: number
  potential_payout: number
  status: string
  contract_address: string | null
  transaction_hash: string | null
  resolution_data: any
  created_at: string
  resolved_at: string | null
}

export const authApi = {
  register: async (email: string, username: string, password: string, walletAddress?: string) => {
    const { data } = await api.post('/auth/register', {
      email,
      username,
      password,
      wallet_address: walletAddress,
    })
    return data
  },
  login: async (email: string, password: string) => {
    const { data } = await api.post('/auth/login', {
      username: email,
      password,
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    if (data.access_token) {
      localStorage.setItem('token', data.access_token)
    }
    return data
  },
  me: async (): Promise<User> => {
    const { data } = await api.get('/auth/me')
    return data
  },
}

export const personalitiesApi = {
  list: async (): Promise<Personality[]> => {
    const { data } = await api.get('/personalities')
    return data
  },
  get: async (id: number): Promise<Personality> => {
    const { data } = await api.get(`/personalities/${id}`)
    return data
  },
  getHistory: async (id: number, days: number = 30) => {
    const { data } = await api.get(`/personalities/${id}/history?days=${days}`)
    return data
  },
}

export const tradesApi = {
  buy: async (personalityId: number, shares: number, transactionHash?: string) => {
    const { data } = await api.post('/trades/buy', {
      personality_id: personalityId,
      trade_type: 'buy',
      shares,
      transaction_hash: transactionHash,
    })
    return data
  },
  sell: async (personalityId: number, shares: number, transactionHash?: string) => {
    const { data } = await api.post('/trades/sell', {
      personality_id: personalityId,
      trade_type: 'sell',
      shares,
      transaction_hash: transactionHash,
    })
    return data
  },
  my: async (): Promise<Trade[]> => {
    const { data } = await api.get('/trades/my')
    return data
  },
}

export const parlaysApi = {
  list: async (): Promise<Parlay[]> => {
    const { data } = await api.get('/parlays')
    return data
  },
  get: async (id: number): Promise<Parlay> => {
    const { data } = await api.get(`/parlays/${id}`)
    return data
  },
  create: async (name: string, legs: Array<{ personality_id: number; direction: 'up' | 'down'; threshold: number }>, stake: number, transactionHash?: string) => {
    const { data } = await api.post('/parlays', {
      name,
      legs,
      total_stake: stake,
      transaction_hash: transactionHash,
    })
    return data
  },
  my: async (): Promise<Parlay[]> => {
    const { data } = await api.get('/parlays/my')
    return data
  },
}

export const mlApi = {
  topGainers: async () => {
    const { data } = await api.get('/ml/signals/top-gainers')
    return data
  },
  topLosers: async () => {
    const { data } = await api.get('/ml/signals/top-losers')
    return data
  },
}

export default api


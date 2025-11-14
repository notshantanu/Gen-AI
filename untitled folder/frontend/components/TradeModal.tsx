'use client'

import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { tradesApi, Personality } from '@/lib/api'
import { useAccount } from 'wagmi'

interface TradeModalProps {
  personality: Personality
  tradeType: 'buy' | 'sell'
  onClose: () => void
}

export function TradeModal({ personality, tradeType, onClose }: TradeModalProps) {
  const [shares, setShares] = useState('')
  const { address } = useAccount()
  const queryClient = useQueryClient()

  const mutation = useMutation({
    mutationFn: (data: { shares: number; transactionHash?: string }) => {
      if (tradeType === 'buy') {
        return tradesApi.buy(personality.id, data.shares, data.transactionHash)
      } else {
        return tradesApi.sell(personality.id, data.shares, data.transactionHash)
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['personality', personality.id] })
      queryClient.invalidateQueries({ queryKey: ['trades'] })
      onClose()
    },
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const sharesNum = parseFloat(shares)
    if (isNaN(sharesNum) || sharesNum <= 0) {
      alert('Please enter a valid number of shares')
      return
    }

    if (!address) {
      alert('Please connect your wallet')
      return
    }

    // In a real implementation, you would:
    // 1. Generate transaction data from smart contract
    // 2. Sign and send transaction
    // 3. Get transaction hash
    // 4. Call API with transaction hash

    // For MVP, we'll just call the API directly
    mutation.mutate({ shares: sharesNum })
  }

  const totalCost = personality.price_per_share
    ? (parseFloat(shares) || 0) * personality.price_per_share
    : 0

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8 max-w-md w-full">
        <h2 className="text-2xl font-bold mb-4">
          {tradeType === 'buy' ? 'Buy' : 'Sell'} {personality.name} Shares
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Number of Shares
            </label>
            <input
              type="number"
              step="0.0001"
              min="0"
              value={shares}
              onChange={(e) => setShares(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              required
            />
          </div>
          {personality.price_per_share && (
            <div className="mb-4">
              <div className="flex justify-between text-sm text-gray-600 mb-1">
                <span>Price per Share:</span>
                <span>{personality.price_per_share.toFixed(4)} AURA</span>
              </div>
              <div className="flex justify-between text-lg font-semibold">
                <span>Total Cost:</span>
                <span>{totalCost.toFixed(4)} AURA</span>
              </div>
            </div>
          )}
          <div className="flex space-x-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 px-4 py-2 rounded-md"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={mutation.isPending}
              className={`flex-1 px-4 py-2 rounded-md text-white ${
                tradeType === 'buy'
                  ? 'bg-green-600 hover:bg-green-700'
                  : 'bg-red-600 hover:bg-red-700'
              } disabled:opacity-50`}
            >
              {mutation.isPending ? 'Processing...' : tradeType === 'buy' ? 'Buy' : 'Sell'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}


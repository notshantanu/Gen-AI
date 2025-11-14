'use client'

import { useQuery } from '@tanstack/react-query'
import { useParams } from 'next/navigation'
import { Navbar } from '@/components/Navbar'
import { personalitiesApi, Personality } from '@/lib/api'
import { TradeModal } from '@/components/TradeModal'
import { useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function PersonalityDetailPage() {
  const params = useParams()
  const id = parseInt(params.id as string)
  const [showTradeModal, setShowTradeModal] = useState(false)
  const [tradeType, setTradeType] = useState<'buy' | 'sell'>('buy')

  const { data: personality, isLoading } = useQuery({
    queryKey: ['personality', id],
    queryFn: () => personalitiesApi.get(id),
  })

  const { data: history } = useQuery({
    queryKey: ['personality-history', id],
    queryFn: () => personalitiesApi.getHistory(id, 30),
    enabled: !!personality,
  })

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">Loading...</div>
        </div>
      </div>
    )
  }

  if (!personality) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">Personality not found</div>
        </div>
      </div>
    )
  }

  const chartData = history?.map((h: any) => ({
    date: new Date(h.timestamp).toLocaleDateString(),
    score: parseFloat(h.score),
    price: parseFloat(h.price_per_share),
  })) || []

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">{personality.name}</h1>
          {personality.description && (
            <p className="text-gray-600 mb-6">{personality.description}</p>
          )}

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-500 mb-1">Current Score</div>
              <div className="text-2xl font-bold">{personality.current_score?.toFixed(2) || 'N/A'}</div>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-500 mb-1">Price per Share</div>
              <div className="text-2xl font-bold">{personality.price_per_share?.toFixed(4) || 'N/A'} AURA</div>
            </div>
            <div className="bg-gray-50 p-4 rounded-lg">
              <div className="text-sm text-gray-500 mb-1">Momentum</div>
              <div className={`text-2xl font-bold ${personality.momentum_score && personality.momentum_score > 0 ? 'text-green-600' : 'text-red-600'}`}>
                {personality.momentum_score ? (personality.momentum_score > 0 ? '+' : '') + personality.momentum_score.toFixed(4) : 'N/A'}
              </div>
            </div>
          </div>

          <div className="flex space-x-4">
            <button
              onClick={() => {
                setTradeType('buy')
                setShowTradeModal(true)
              }}
              className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium"
            >
              Buy Shares
            </button>
            <button
              onClick={() => {
                setTradeType('sell')
                setShowTradeModal(true)
              }}
              className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-lg font-medium"
            >
              Sell Shares
            </button>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Price History (30 days)</h2>
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="price" stroke="#0ea5e9" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {showTradeModal && (
          <TradeModal
            personality={personality}
            tradeType={tradeType}
            onClose={() => setShowTradeModal(false)}
          />
        )}
      </main>
    </div>
  )
}


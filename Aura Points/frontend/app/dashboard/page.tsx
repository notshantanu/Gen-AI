'use client'

import { useQuery } from '@tanstack/react-query'
import { Navbar } from '@/components/Navbar'
import { tradesApi, mlApi, Trade } from '@/lib/api'
import Link from 'next/link'

export default function DashboardPage() {
  const { data: trades } = useQuery({
    queryKey: ['trades'],
    queryFn: () => tradesApi.my(),
  })

  const { data: topGainers } = useQuery({
    queryKey: ['top-gainers'],
    queryFn: () => mlApi.topGainers(),
  })

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">My Trades</h2>
            {trades && trades.length > 0 ? (
              <div className="space-y-4">
                {trades.slice(0, 10).map((trade: Trade) => (
                  <div key={trade.id} className="border-b pb-4">
                    <div className="flex justify-between items-center">
                      <div>
                        <span className={`font-semibold ${trade.trade_type === 'buy' ? 'text-green-600' : 'text-red-600'}`}>
                          {trade.trade_type.toUpperCase()}
                        </span>
                        <span className="text-gray-600 ml-2">
                          {trade.shares} shares
                        </span>
                      </div>
                      <div className="text-right">
                        <div className="font-semibold">{trade.total_cost.toFixed(4)} AURA</div>
                        <div className="text-sm text-gray-500">
                          {new Date(trade.created_at).toLocaleDateString()}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No trades yet</p>
            )}
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Top Momentum Picks</h2>
            {topGainers?.personalities && topGainers.personalities.length > 0 ? (
              <div className="space-y-4">
                {topGainers.personalities.slice(0, 5).map((personality: any) => (
                  <Link
                    key={personality.personality_id}
                    href={`/personalities/${personality.personality_id}`}
                    className="block border-b pb-4 hover:bg-gray-50 p-2 rounded"
                  >
                    <div className="flex justify-between items-center">
                      <div>
                        <div className="font-semibold">{personality.personality_name}</div>
                        <div className="text-sm text-gray-500">
                          Momentum: {personality.momentum_score > 0 ? '+' : ''}
                          {parseFloat(personality.momentum_score).toFixed(4)}
                        </div>
                      </div>
                      <div className="text-green-600 font-semibold">
                        ↗
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No data available</p>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}


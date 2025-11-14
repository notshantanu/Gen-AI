'use client'

import { useQuery } from '@tanstack/react-query'
import { Navbar } from '@/components/Navbar'
import { personalitiesApi, Personality } from '@/lib/api'
import Link from 'next/link'

export default function PersonalitiesPage() {
  const { data: personalities, isLoading } = useQuery({
    queryKey: ['personalities'],
    queryFn: () => personalitiesApi.list(),
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

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">All Personalities</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {personalities?.map((personality: Personality) => (
            <Link
              key={personality.id}
              href={`/personalities/${personality.id}`}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
            >
              <h2 className="text-xl font-semibold mb-2">{personality.name}</h2>
              {personality.description && (
                <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                  {personality.description}
                </p>
              )}
              <div className="space-y-2">
                {personality.current_score && (
                  <div className="flex justify-between">
                    <span className="text-gray-500">Current Score:</span>
                    <span className="font-semibold">{personality.current_score.toFixed(2)}</span>
                  </div>
                )}
                {personality.price_per_share && (
                  <div className="flex justify-between">
                    <span className="text-gray-500">Price/Share:</span>
                    <span className="font-semibold">{personality.price_per_share.toFixed(4)} AURA</span>
                  </div>
                )}
                {personality.momentum_score && (
                  <div className="flex justify-between">
                    <span className="text-gray-500">Momentum:</span>
                    <span className={`font-semibold ${personality.momentum_score > 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {personality.momentum_score > 0 ? '+' : ''}{personality.momentum_score.toFixed(4)}
                    </span>
                  </div>
                )}
              </div>
            </Link>
          ))}
        </div>
      </main>
    </div>
  )
}


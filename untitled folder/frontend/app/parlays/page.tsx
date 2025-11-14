'use client'

import { useQuery } from '@tanstack/react-query'
import { Navbar } from '@/components/Navbar'
import { parlaysApi, Parlay } from '@/lib/api'
import Link from 'next/link'
import { useState } from 'react'

export default function ParlaysPage() {
  const [showCreateModal, setShowCreateModal] = useState(false)
  const { data: parlays } = useQuery({
    queryKey: ['parlays'],
    queryFn: () => parlaysApi.list(),
  })

  const { data: myParlays } = useQuery({
    queryKey: ['my-parlays'],
    queryFn: () => parlaysApi.my(),
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'won':
        return 'text-green-600'
      case 'lost':
        return 'text-red-600'
      case 'active':
        return 'text-blue-600'
      default:
        return 'text-gray-600'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Parlays</h1>
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-3 rounded-lg font-medium"
          >
            Create Parlay
          </button>
        </div>

        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">My Parlays</h2>
          {myParlays && myParlays.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {myParlays.map((parlay: Parlay) => (
                <div key={parlay.id} className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-lg font-semibold mb-2">{parlay.name}</h3>
                  <div className="space-y-2 mb-4">
                    <div className="flex justify-between">
                      <span className="text-gray-500">Stake:</span>
                      <span className="font-semibold">{parlay.total_stake} AURA</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Potential Payout:</span>
                      <span className="font-semibold text-green-600">{parlay.potential_payout} AURA</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Status:</span>
                      <span className={`font-semibold ${getStatusColor(parlay.status)}`}>
                        {parlay.status.toUpperCase()}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Legs:</span>
                      <span className="font-semibold">{parlay.legs.length}</span>
                    </div>
                  </div>
                  <div className="text-sm text-gray-500">
                    Created: {new Date(parlay.created_at).toLocaleDateString()}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500">No parlays yet</p>
          )}
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-4">All Parlays</h2>
          {parlays && parlays.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {parlays.map((parlay: Parlay) => (
                <div key={parlay.id} className="bg-white rounded-lg shadow-md p-6">
                  <h3 className="text-lg font-semibold mb-2">{parlay.name}</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-gray-500">Stake:</span>
                      <span className="font-semibold">{parlay.total_stake} AURA</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Potential Payout:</span>
                      <span className="font-semibold text-green-600">{parlay.potential_payout} AURA</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-500">Status:</span>
                      <span className={`font-semibold ${getStatusColor(parlay.status)}`}>
                        {parlay.status.toUpperCase()}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500">No parlays available</p>
          )}
        </div>
      </main>
    </div>
  )
}


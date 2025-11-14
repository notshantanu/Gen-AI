import { Navbar } from '@/components/Navbar'
import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-5xl font-extrabold text-gray-900 sm:text-6xl">
            Aura Points
          </h1>
          <p className="mt-6 text-xl text-gray-600 max-w-3xl mx-auto">
            Trade aura points for real-world personalities. Powered by blockchain and machine learning.
          </p>
          <div className="mt-10 flex justify-center space-x-4">
            <Link
              href="/personalities"
              className="bg-primary-600 hover:bg-primary-700 text-white px-8 py-3 rounded-lg text-lg font-medium"
            >
              Explore Personalities
            </Link>
            <Link
              href="/dashboard"
              className="bg-white hover:bg-gray-50 text-primary-600 border-2 border-primary-600 px-8 py-3 rounded-lg text-lg font-medium"
            >
              View Dashboard
            </Link>
          </div>
        </div>

        <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-2">Blockchain Trading</h3>
            <p className="text-gray-600">
              Buy and sell aura points using smart contracts on the blockchain.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-2">ML Predictions</h3>
            <p className="text-gray-600">
              Get momentum predictions powered by machine learning and social media signals.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-2">Parlays</h3>
            <p className="text-gray-600">
              Create multi-leg parlays for higher risk and reward opportunities.
            </p>
          </div>
        </div>
      </main>
    </div>
  )
}


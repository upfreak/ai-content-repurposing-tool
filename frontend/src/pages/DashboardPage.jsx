import { useEffect, useState } from 'react'
import { contentService } from '../services/contentService'
import { BarChart3, FileText, Zap } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

export default function DashboardPage() {
  const navigate = useNavigate()
  const [stats, setStats] = useState({
    contentCount: 0,
    generationCount: 0,
    recentContent: [],
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboard()
  }, [])

  const fetchDashboard = async () => {
    try {
      const contentRes = await contentService.listContent(0, 5)
      const historyRes = await contentService.getGenerationHistory(0, 5)

      setStats({
        contentCount: contentRes.data.length,
        generationCount: historyRes.data.length,
        recentContent: contentRes.data,
      })
    } catch (error) {
      console.error('Failed to fetch dashboard', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Total Content</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {stats.contentCount}
              </p>
            </div>
            <FileText className="w-12 h-12 text-blue-600 opacity-20" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Generated Pieces</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">
                {stats.generationCount}
              </p>
            </div>
            <Zap className="w-12 h-12 text-purple-600 opacity-20" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 text-sm font-medium">Usage</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">Free Plan</p>
            </div>
            <BarChart3 className="w-12 h-12 text-green-600 opacity-20" />
          </div>
        </div>
      </div>

      {/* Recent Content */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Content */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Content</h2>
          {stats.recentContent.length === 0 ? (
            <p className="text-gray-600 text-center py-8">No content yet</p>
          ) : (
            <div className="space-y-4">
              {stats.recentContent.map((content) => (
                <div
                  key={content.id}
                  className="border border-gray-200 rounded p-4 hover:bg-gray-50 cursor-pointer transition"
                  onClick={() => navigate(`/new-project?content=${content.id}`)}
                >
                  <h3 className="font-medium text-gray-900">
                    {content.title || 'Untitled'}
                  </h3>
                  <p className="text-sm text-gray-600 mt-1">
                    {content.word_count} words
                  </p>
                </div>
              ))}
            </div>
          )}

          <button
            onClick={() => navigate('/content-library')}
            className="w-full mt-6 py-2 px-4 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition font-medium"
          >
            View All Content
          </button>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>

          <div className="space-y-3">
            <button
              onClick={() => navigate('/new-project')}
              className="w-full py-3 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
            >
              New Project
            </button>
            <button
              onClick={() => navigate('/settings')}
              className="w-full py-3 px-4 border border-gray-300 text-gray-900 rounded-lg hover:bg-gray-50 transition font-medium"
            >
              Brand Voices & Settings
            </button>
          </div>

          <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
            <h3 className="font-medium text-blue-900 mb-2">How to Get Started</h3>
            <ol className="text-sm text-blue-800 space-y-2 list-decimal list-inside">
              <li>Upload or paste your content</li>
              <li>Select platforms and tone</li>
              <li>Generate repurposed content</li>
              <li>Copy and publish</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  )
}

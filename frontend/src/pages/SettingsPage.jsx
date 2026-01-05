import { useState, useEffect } from 'react'
import { Plus, Trash2 } from 'lucide-react'
import toast from 'react-hot-toast'
import apiClient from '../services/api'

export default function SettingsPage() {
  const [brandVoices, setBrandVoices] = useState([])
  const [loading, setLoading] = useState(false)
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    instructions: '',
  })

  useEffect(() => {
    fetchBrandVoices()
  }, [])

  const fetchBrandVoices = async () => {
    try {
      const response = await apiClient.get('/api/user/brand-voices')
      setBrandVoices(response.data)
    } catch (error) {
      toast.error('Failed to load brand voices')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      await apiClient.post('/api/user/brand-voice', formData)
      toast.success('Brand voice created')
      setFormData({ name: '', instructions: '' })
      setShowForm(false)
      fetchBrandVoices()
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to create brand voice')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this brand voice?')) return

    try {
      await apiClient.delete(`/api/user/brand-voice/${id}`)
      toast.success('Brand voice deleted')
      fetchBrandVoices()
    } catch (error) {
      toast.error('Failed to delete brand voice')
    }
  }

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">Settings</h1>

      {/* Brand Voices */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Brand Voices</h2>
          <button
            onClick={() => setShowForm(!showForm)}
            className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            <Plus className="w-5 h-5" />
            <span>New Brand Voice</span>
          </button>
        </div>

        {/* Form */}
        {showForm && (
          <form onSubmit={handleSubmit} className="mb-8 p-6 bg-gray-50 rounded-lg">
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Name
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) =>
                    setFormData({ ...formData, name: e.target.value })
                  }
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., Professional Brand"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Instructions
                </label>
                <textarea
                  value={formData.instructions}
                  onChange={(e) =>
                    setFormData({ ...formData, instructions: e.target.value })
                  }
                  required
                  rows={4}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 resize-none"
                  placeholder="Describe your brand voice, tone, style, and any specific instructions..."
                />
              </div>

              <div className="flex space-x-3">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 py-2 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
                >
                  {loading ? 'Creating...' : 'Create'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowForm(false)
                    setFormData({ name: '', instructions: '' })
                  }}
                  className="flex-1 py-2 px-4 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-100 transition"
                >
                  Cancel
                </button>
              </div>
            </div>
          </form>
        )}

        {/* List */}
        <div className="space-y-4">
          {brandVoices.length === 0 ? (
            <p className="text-gray-600 text-center py-8">
              No brand voices yet. Create one to get started!
            </p>
          ) : (
            brandVoices.map((voice) => (
              <div
                key={voice.id}
                className="border border-gray-200 rounded-lg p-4 flex items-start justify-between"
              >
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900">{voice.name}</h3>
                  <p className="text-sm text-gray-600 mt-1">{voice.instructions}</p>
                </div>
                <button
                  onClick={() => handleDelete(voice.id)}
                  className="p-2 rounded hover:bg-red-50 text-red-600 ml-4"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}

import { useState, useEffect } from 'react'
import { CheckCircle, RefreshCw, Copy, Trash2 } from 'lucide-react'
import { contentService } from '../../services/contentService'
import toast from 'react-hot-toast'

const PLATFORMS = [
  { id: 'twitter', label: 'Twitter/X', icon: '𝕏' },
  { id: 'linkedin', label: 'LinkedIn', icon: '💼' },
  { id: 'instagram', label: 'Instagram', icon: '📸' },
  { id: 'facebook', label: 'Facebook', icon: '👍' },
  { id: 'tiktok', label: 'TikTok', icon: '🎬' },
  { id: 'email', label: 'Email', icon: '📧' },
  { id: 'summary', label: 'Summary', icon: '📄' },
]

const TONES = [
  'Professional',
  'Casual',
  'Enthusiastic',
  'Educational',
  'Humorous',
]

export default function GenerationForm({ content, onSuccess }) {
  const [selectedPlatforms, setSelectedPlatforms] = useState([])
  const [selectedTone, setSelectedTone] = useState('Professional')
  const [loading, setLoading] = useState(false)
  const [generations, setGenerations] = useState([])
  
  const togglePlatform = (platformId) => {
    setSelectedPlatforms((prev) =>
      prev.includes(platformId)
        ? prev.filter((id) => id !== platformId)
        : [...prev, platformId]
    )
  }
  
  const handleGenerate = async () => {
    if (selectedPlatforms.length === 0) {
      toast.error('Please select at least one platform')
      return
    }
    
    setLoading(true)
    try {
      const response = await contentService.repurposeContent(
        content.id,
        selectedPlatforms,
        selectedTone,
        null
      )
      
      setGenerations(response.data.generations || [])
      toast.success('Content generated successfully!')
      onSuccess?.(response.data)
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Generation failed')
    } finally {
      setLoading(false)
    }
  }
  
  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
    toast.success('Copied to clipboard!')
  }
  
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold mb-6">Generate Content</h2>
      
      {/* Tone Selection */}
      <div className="mb-8">
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Select Tone
        </label>
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
          {TONES.map((tone) => (
            <button
              key={tone}
              onClick={() => setSelectedTone(tone)}
              className={`py-2 px-3 rounded-lg font-medium transition ${
                selectedTone === tone
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {tone}
            </button>
          ))}
        </div>
      </div>
      
      {/* Platform Selection */}
      <div className="mb-8">
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Select Platforms
        </label>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {PLATFORMS.map((platform) => (
            <button
              key={platform.id}
              onClick={() => togglePlatform(platform.id)}
              className={`py-3 px-4 rounded-lg font-medium transition flex items-center justify-center space-x-2 ${
                selectedPlatforms.includes(platform.id)
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <span>{platform.icon}</span>
              <span>{platform.label}</span>
            </button>
          ))}
        </div>
      </div>
      
      {/* Generate Button */}
      <button
        onClick={handleGenerate}
        disabled={loading || selectedPlatforms.length === 0}
        className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 font-medium"
      >
        {loading ? 'Generating...' : 'Generate Content'}
      </button>
      
      {/* Generated Content */}
      {generations.length > 0 && (
        <div className="mt-8 space-y-4">
          <h3 className="text-xl font-bold">Generated Content</h3>
          {generations.map((gen) => (
            <div key={gen.id} className="border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  <span className="font-medium text-gray-900">{gen.platform}</span>
                </div>
                <button
                  onClick={() => copyToClipboard(gen.generated_text)}
                  className="p-2 rounded hover:bg-gray-100"
                >
                  <Copy className="w-5 h-5 text-gray-600" />
                </button>
              </div>
              <div className="bg-gray-50 rounded p-3 mb-3 max-h-40 overflow-y-auto">
                <p className="text-gray-700 text-sm">{gen.generated_text}</p>
              </div>
              <div className="flex space-x-2">
                <button className="flex-1 flex items-center justify-center space-x-2 py-2 px-3 rounded border border-gray-300 hover:bg-gray-50 transition">
                  <RefreshCw className="w-4 h-4" />
                  <span>Regenerate</span>
                </button>
                <button
                  onClick={() => {}}
                  className="flex items-center justify-center py-2 px-3 rounded border border-red-300 text-red-600 hover:bg-red-50 transition"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

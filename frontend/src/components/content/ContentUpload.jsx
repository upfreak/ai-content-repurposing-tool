import { Upload, Link as LinkIcon, FileText } from 'lucide-react'
import { useState } from 'react'
import toast from 'react-hot-toast'
import { contentService } from '../../services/contentService'

export default function ContentUpload({ onSuccess }) {
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('text')
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    url: '',
    file: null,
  })

  const handleTextSubmit = async (e) => {
    e.preventDefault()

    if (!formData.content.trim()) {
      toast.error('Please enter content')
      return
    }

    setLoading(true)
    try {
      const response = await contentService.uploadContent(
        formData.title || 'Untitled',
        formData.content,
        'text'
      )

      toast.success('Content uploaded successfully')
      setFormData({ title: '', content: '', url: '', file: null })
      onSuccess(response.data)
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  const handleUrlSubmit = async (e) => {
    e.preventDefault()

    if (!formData.url.trim()) {
      toast.error('Please enter a URL')
      return
    }

    setLoading(true)
    try {
      const response = await contentService.uploadContent(
        formData.title || 'Untitled',
        formData.url,
        'url'
      )

      toast.success('Content imported successfully')
      setFormData({ title: '', content: '', url: '', file: null })
      onSuccess(response.data)
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Import failed')
    } finally {
      setLoading(false)
    }
  }

  const handleFileSubmit = async (e) => {
    e.preventDefault()

    if (!formData.file) {
      toast.error('Please select a file')
      return
    }

    setLoading(true)
    try {
      const response = await contentService.uploadFile(
        formData.title || formData.file.name,
        formData.file
      )

      toast.success('File uploaded successfully')
      setFormData({ title: '', content: '', url: '', file: null })
      onSuccess(response.data)
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold mb-6">Upload Content</h2>

      <div className="flex space-x-4 mb-6 border-b">
        <button
          onClick={() => setActiveTab('text')}
          className={`pb-2 font-medium ${activeTab === 'text'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-900'
            }`}
        >
          <FileText className="w-4 h-4 inline mr-2" />
          Paste Text
        </button>
        <button
          onClick={() => setActiveTab('url')}
          className={`pb-2 font-medium ${activeTab === 'url'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-900'
            }`}
        >
          <LinkIcon className="w-4 h-4 inline mr-2" />
          Import URL
        </button>
        <button
          onClick={() => setActiveTab('file')}
          className={`pb-2 font-medium ${activeTab === 'file'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-900'
            }`}
        >
          <Upload className="w-4 h-4 inline mr-2" />
          Upload File
        </button>
      </div>

      {/* Text Tab */}
      {activeTab === 'text' && (
        <form onSubmit={handleTextSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Content title (optional)"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />

          <textarea
            placeholder="Paste your blog post, article, or transcript here..."
            value={formData.content}
            onChange={(e) => setFormData({ ...formData, content: e.target.value })}
            rows={10}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 resize-none"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
          >
            {loading ? 'Uploading...' : 'Upload Content'}
          </button>
        </form>
      )}

      {/* URL Tab */}
      {activeTab === 'url' && (
        <form onSubmit={handleUrlSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Content title (optional)"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />

          <input
            type="url"
            placeholder="https://example.com/blog-post"
            value={formData.url}
            onChange={(e) => setFormData({ ...formData, url: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
          >
            {loading ? 'Importing...' : 'Import Content'}
          </button>
        </form>
      )}

      {/* File Tab */}
      {activeTab === 'file' && (
        <form onSubmit={handleFileSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="Content title (optional)"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          />

          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6">
            <input
              type="file"
              accept=".txt,.md,.pdf,.docx"
              onChange={(e) =>
                setFormData({ ...formData, file: e.target.files?.[0] || null })
              }
              className="w-full"
            />
            <p className="text-sm text-gray-600 mt-2">
              Supported: .txt, .md, .pdf, .docx
            </p>
          </div>

          {formData.file && (
            <p className="text-sm text-gray-700">
              Selected: {formData.file.name}
            </p>
          )}

          <button
            type="submit"
            disabled={loading || !formData.file}
            className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
          >
            {loading ? 'Uploading...' : 'Upload File'}
          </button>
        </form>
      )}
    </div>
  )
}

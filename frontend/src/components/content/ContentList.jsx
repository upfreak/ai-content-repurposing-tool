import { useEffect, useState } from 'react'
import { contentService } from '../../services/contentService'
import { Trash2 } from 'lucide-react'
import toast from 'react-hot-toast'

export default function ContentList() {
  const [contents, setContents] = useState([])
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    fetchContents()
  }, [])
  
  const fetchContents = async () => {
    try {
      const response = await contentService.listContent()
      setContents(response.data)
    } catch (error) {
      toast.error('Failed to load content')
    } finally {
      setLoading(false)
    }
  }
  
  const handleDelete = async (contentId) => {
    if (!window.confirm('Are you sure?')) return
    
    try {
      await contentService.deleteContent(contentId)
      setContents((prev) => prev.filter((c) => c.id !== contentId))
      toast.success('Content deleted')
    } catch (error) {
      toast.error('Failed to delete content')
    }
  }
  
  if (loading) {
    return <div className="text-center py-8">Loading...</div>
  }
  
  return (
    <div className="bg-white rounded-lg shadow-md">
      <div className="p-6">
        <h2 className="text-2xl font-bold mb-6">Your Content</h2>
        
        {contents.length === 0 ? (
          <p className="text-gray-600 text-center py-8">No content yet</p>
        ) : (
          <div className="space-y-4">
            {contents.map((content) => (
              <div
                key={content.id}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900">
                      {content.title || 'Untitled'}
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {content.word_count} words •{' '}
                      {new Date(content.created_at).toLocaleDateString()}
                    </p>
                    <p className="text-sm text-gray-700 mt-2 line-clamp-2">
                      {content.original_content}
                    </p>
                  </div>
                  <button
                    onClick={() => handleDelete(content.id)}
                    className="p-2 rounded hover:bg-red-50 text-red-600 ml-4"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

import { useState } from 'react'
import ContentUpload from '../components/content/ContentUpload'
import GenerationForm from '../components/generation/GenerationForm'

export default function NewProjectPage() {
  const [selectedContent, setSelectedContent] = useState(null)
  
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">New Project</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <ContentUpload onSuccess={setSelectedContent} />
        
        {selectedContent && (
          <div>
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Selected Content
              </h3>
              <div className="bg-blue-50 border border-blue-200 rounded p-4">
                <h4 className="font-medium text-gray-900">
                  {selectedContent.title || 'Untitled'}
                </h4>
                <p className="text-sm text-gray-600 mt-2">
                  {selectedContent.word_count} words
                </p>
                <p className="text-sm text-gray-700 mt-3 line-clamp-5">
                  {selectedContent.original_content}
                </p>
              </div>
            </div>
            
            <GenerationForm content={selectedContent} />
          </div>
        )}
      </div>
    </div>
  )
}

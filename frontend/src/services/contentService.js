import apiClient from './api'

export const contentService = {
  uploadContent: (title, originalContent, contentType) =>
    apiClient.post('/api/content/upload', {
      title,
      original_content: originalContent,
      content_type: contentType,
    }),

  uploadFile: (title, file) => {
    const formData = new FormData()
    formData.append('title', title)
    formData.append('file', file)
    return apiClient.post('/api/content/upload-file', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  listContent: (skip = 0, limit = 20) =>
    apiClient.get('/api/content/', { params: { skip, limit } }),

  getContent: (contentId) =>
    apiClient.get(`/api/content/${contentId}`),

  deleteContent: (contentId) =>
    apiClient.delete(`/api/content/${contentId}`),

  repurposeContent: (contentId, platforms, tone, brandVoiceId) =>
    apiClient.post('/api/generate/repurpose', {
      content_id: contentId,
      platforms,
      tone,
      brand_voice_id: brandVoiceId,
    }),

  getGenerationHistory: (skip = 0, limit = 50) =>
    apiClient.get('/api/generate/history', { params: { skip, limit } }),

  regenerateContent: (generationId, tone) =>
    apiClient.post(`/api/generate/regenerate/${generationId}`, { tone }),

  deleteGeneration: (generationId) =>
    apiClient.delete(`/api/generate/${generationId}`),
}

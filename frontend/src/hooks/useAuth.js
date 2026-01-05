import { useEffect, useState } from 'react'
import { useAuthStore } from '../store'
import apiClient from '../services/api'

export const useAuth = () => {
  const { user, isAuthenticated, setUser, logout } = useAuthStore()
  const [loading, setLoading] = useState(true)
  
  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      // Try to fetch user profile
      apiClient
        .get('/api/user/profile')
        .then((res) => {
          setUser(res.data)
        })
        .catch(() => {
          logout()
        })
        .finally(() => {
          setLoading(false)
        })
    } else {
      setLoading(false)
    }
  }, [setUser, logout])
  
  return { user, isAuthenticated, loading }
}

export const useContent = () => {
  const { contents, selectedContent, setContents, setSelectedContent } =
    useAuthStore((state) => ({
      contents: state.contents || [],
      selectedContent: state.selectedContent,
      setContents: state.setContents,
      setSelectedContent: state.setSelectedContent,
    }))
  
  return { contents, selectedContent, setContents, setSelectedContent }
}

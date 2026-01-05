import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authService } from '../../services/authService'
import apiClient from '../../services/api'
import { useAuthStore } from '../../store'
import toast from 'react-hot-toast'

export default function LoginForm() {
  const navigate = useNavigate()
  const { setUser, initAuth } = useAuthStore()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    console.log('🔵 Login form submitted')

    try {
      console.log('🔵 Calling login API...')
      const response = await authService.login(formData.email, formData.password)
      console.log('✅ Login API response:', response.data)

      // Save tokens
      localStorage.setItem('access_token', response.data.access_token)
      localStorage.setItem('refresh_token', response.data.refresh_token)
      localStorage.setItem('user_email', formData.email)
      console.log('✅ Tokens saved to localStorage')

      // Immediately set a placeholder user so isAuthenticated is true
      setUser({ email: formData.email })
      console.log('✅ Placeholder user set in store')

      toast.success('Login successful!')
      console.log('🔵 About to navigate to /dashboard')

      // Navigate immediately (don't wait for profile fetch)
      navigate('/dashboard')
      console.log('✅ Navigate called')

      // Fetch actual user profile in background
      try {
        const profileRes = await apiClient.get('/api/user/profile')
        setUser(profileRes.data)
        console.log('✅ User profile fetched and updated')
      } catch (profileErr) {
        console.warn('⚠️ Failed to fetch profile after login', profileErr)
      }
    } catch (error) {
      console.error('❌ Login error:', error)
      toast.error(error.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="you@example.com"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="••••••••"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
      >
        {loading ? 'Signing in...' : 'Sign In'}
      </button>
    </form>
  )
}

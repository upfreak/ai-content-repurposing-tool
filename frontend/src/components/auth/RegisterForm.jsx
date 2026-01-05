import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authService } from '../../services/authService'
import apiClient from '../../services/api'
import { useAuthStore } from '../../store'
import toast from 'react-hot-toast'

export default function RegisterForm() {
  const navigate = useNavigate()
  const { initAuth } = useAuthStore()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    confirmPassword: '',
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (formData.password !== formData.confirmPassword) {
      toast.error('Passwords do not match')
      return
    }

    setLoading(true)

    try {
      // Step 1: Register the user
      await authService.register(
        formData.email,
        formData.username,
        formData.password
      )

      toast.success('Account created successfully!')

      // Step 2: Auto login after successful registration
      try {
        const loginResponse = await authService.login(formData.email, formData.password)

        localStorage.setItem('access_token', loginResponse.data.access_token)
        localStorage.setItem('refresh_token', loginResponse.data.refresh_token)
        localStorage.setItem('user_email', formData.email)

        // Immediately set placeholder user so isAuthenticated is true
        useAuthStore.getState().setUser({ email: formData.email, username: formData.username })

        // Navigate immediately
        navigate('/dashboard')

        // Fetch full profile in background
        try {
          const profileRes = await apiClient.get('/api/user/profile')
          useAuthStore.getState().setUser(profileRes.data)
        } catch (err) {
          console.warn('Failed to fetch profile after register+login', err)
        }
      } catch (loginError) {
        console.error('Auto-login failed:', loginError)
        toast.error('Account created! Please login.')

        // Use navigate instead of window.location.href
        setTimeout(() => {
          navigate('/login')
        }, 1500)
      }
    } catch (error) {
      console.error('Registration error:', error)
      toast.error(error.response?.data?.detail || 'Registration failed')
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
        <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
        <input
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
          required
          minLength={3}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Choose a username"
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
          minLength={8}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="••••••••"
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Confirm Password</label>
        <input
          type="password"
          name="confirmPassword"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
          minLength={8}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="••••••••"
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
      >
        {loading ? 'Creating account...' : 'Create Account'}
      </button>
    </form>
  )
}

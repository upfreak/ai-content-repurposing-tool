import { useNavigate, Link } from 'react-router-dom'
import { useEffect } from 'react'
import RegisterForm from '../components/auth/RegisterForm'
import { Zap } from 'lucide-react'

export default function RegisterPage() {
  const navigate = useNavigate()

  // Redirect to dashboard if already logged in
  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      navigate('/dashboard', { replace: true })
    }
  }, [navigate])

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-lg shadow-xl p-8">
          <div className="flex items-center justify-center space-x-2 mb-8">
            <Zap className="w-8 h-8 text-blue-600" />
            <h1 className="text-2xl font-bold text-gray-900">RepurposeAI</h1>
          </div>

          <h2 className="text-3xl font-bold text-gray-900 mb-2 text-center">
            Create Account
          </h2>
          <p className="text-gray-600 text-center mb-8">
            Get started with RepurposeAI today
          </p>

          <RegisterForm />

          <p className="text-center text-gray-600 mt-6">
            Already have an account?{' '}
            <Link to="/login" className="text-blue-600 hover:underline font-medium">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

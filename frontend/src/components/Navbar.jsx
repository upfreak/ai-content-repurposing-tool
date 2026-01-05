import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store'
import { Menu, LogOut, Settings, Zap } from 'lucide-react'
import { useState } from 'react'

export default function Navbar() {
  const navigate = useNavigate()
  const logout = useAuthStore((state) => state.logout)
  const user = useAuthStore((state) => state.user)
  const [isOpen, setIsOpen] = useState(false)
  
  const handleLogout = () => {
    logout()
    navigate('/login', { replace: true })
  }
  
  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center space-x-8">
            <div className="flex items-center space-x-2 cursor-pointer" onClick={() => navigate('/dashboard')}>
              <Zap className="w-6 h-6 text-blue-600" />
              <span className="text-xl font-bold text-gray-900">RepurposeAI</span>
            </div>
            
            <div className="hidden md:flex space-x-8">
              <button
                onClick={() => navigate('/dashboard')}
                className="text-gray-700 hover:text-blue-600 transition"
              >
                Dashboard
              </button>
              <button
                onClick={() => navigate('/new-project')}
                className="text-gray-700 hover:text-blue-600 transition"
              >
                New Project
              </button>
              <button
                onClick={() => navigate('/content-library')}
                className="text-gray-700 hover:text-blue-600 transition"
              >
                Library
              </button>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-700">{user?.username}</span>
            <button
              onClick={() => navigate('/settings')}
              className="p-2 rounded-lg hover:bg-gray-100 transition"
            >
              <Settings className="w-5 h-5 text-gray-700" />
            </button>
            <button
              onClick={handleLogout}
              className="p-2 rounded-lg hover:bg-gray-100 transition"
            >
              <LogOut className="w-5 h-5 text-gray-700" />
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}

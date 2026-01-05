import { Toaster } from 'react-hot-toast'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useEffect } from 'react'
import apiClient from './services/api'
import { useAuthStore } from './store'

// Pages
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import NewProjectPage from './pages/NewProjectPage'
import ContentLibraryPage from './pages/ContentLibraryPage'
import SettingsPage from './pages/SettingsPage'

// Components
import ProtectedRoute from './components/ProtectedRoute'

import './index.css'

function App() {
  const setUser = useAuthStore((state) => state.setUser)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      apiClient
        .get('/api/user/profile')
        .then((res) => setUser(res.data))
        .catch(() => {
          // If fetching profile fails, clear stored auth
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
        })
    }
  }, [setUser])
  return (
    <Router>
      <Toaster position="top-right" />
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* Protected routes */}
        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/new-project" element={<NewProjectPage />} />
          <Route path="/content-library" element={<ContentLibraryPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>

        {/* Default redirect */}
        <Route path="/" element={
          localStorage.getItem('access_token') ?
            <Navigate to="/dashboard" replace /> :
            <Navigate to="/login" replace />
        } />
      </Routes>
    </Router>
  )
}

export default App

import { Navigate, Outlet } from 'react-router-dom'
import Navbar from './Navbar'

export default function ProtectedRoute() {
  // Simple check - if no token, redirect to login
  const hasToken = !!localStorage.getItem('access_token')

  if (!hasToken) {
    return <Navigate to="/login" replace />
  }

  return (
    <div className="flex flex-col h-screen">
      <Navbar />
      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>
    </div>
  )
}

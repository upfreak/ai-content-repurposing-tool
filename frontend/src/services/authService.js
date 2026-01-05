import apiClient from './api'

export const authService = {
  register: (email, username, password) =>
    apiClient.post('/api/auth/register', { email, username, password }),

  login: (email, password) =>
    apiClient.post('/api/auth/login', { email, password }),

  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  },
}

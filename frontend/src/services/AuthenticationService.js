import net from './NetworkService'
import router from '../Router/index'
import ENDPOINTS from '../constants/endpoints'

let session = null
export const login = async (email, password) => {
  try {
    const response = await net.post(ENDPOINTS.LOGIN, {
      email,
      password
    })

    const token = response.data.access_token

    // Store token and user in localStorage
    localStorage.setItem('token', token)
    localStorage.setItem('login_time', new Date().toISOString()) // track login time

    // Set token in axios headers
    net.defaults.headers.common.Authorization = `Bearer ${token}`

    // Check every 5 minutes (300,000ms)
    session = setInterval(isAuthenticated, 300000)

    // Navigate to dashboard
    router.push('/')
  } catch (err) {
    console.error('Login failed', err)
    throw err
  }
}

export const logout = () => {
  clearInterval(session)
  localStorage.removeItem('token')
  localStorage.removeItem('email')
  localStorage.removeItem('login_time')
  delete net.defaults.headers.common.Authorization
  router.push('/login')
}

export const signup = async (name, email, password) => {
  try {
    await net.post(ENDPOINTS.REGISTER, { name, email, password })
    // Optionally auto-login
  } catch (err) {
    console.error('Signup failed', err)
    throw err
  }
}

export const isAuthenticated = async () => {
  const token = localStorage.getItem('token')
  const loginTime = new Date(localStorage.getItem('login_time'))
  const now = new Date()
  const elapsed = (now - loginTime) / 1000 / 60 // minutes

  if (!token || elapsed >= 30) {
    console.warn('Token expired or not found')
    logout()
    return false
  }

  try {
    // Ping server to confirm token validity
    const res = await net.get('/auth/me', {
      headers: { Authorization: `Bearer ${token}` }
    })
    return !!res.data
  } catch (err) {
    console.warn('Invalid token or session', err)
    logout()
    return false
  }
}

export const currentUser = async () => {
  try {
    const res = await net.get('/auth/me', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
    return res.data
  } catch (err) {
    logout()
    return null
  }
}

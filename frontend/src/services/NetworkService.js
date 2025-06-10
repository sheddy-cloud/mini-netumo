import axios from 'axios'
import { API_URL } from '../constants/endpoints'
import router from '../Router/index'

const net = axios.create({
  baseURL: API_URL,
  timeout: 100000,
  headers: {}
})

// Axios response interceptor
net.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      // Redirect to login page if not already there
      if (router.currentRoute.value.path !== '/login') {
        router.push('/login')
      }
    }
    return Promise.reject(error)
  }
)

const token = localStorage.getItem('token')

if (token != null) {
  net.defaults.headers.common.Authorization = `Bearer ${token}`
}

export default net

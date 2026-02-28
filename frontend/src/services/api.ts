import axios, { AxiosError, AxiosRequestConfig, CancelTokenSource } from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    const message = (error.response?.data as { message?: string })?.message || error.message || 'An error occurred'
    return Promise.reject(new Error(message))
  }
)

export function createCancelToken(): CancelTokenSource {
  return axios.CancelToken.source()
}

export default api

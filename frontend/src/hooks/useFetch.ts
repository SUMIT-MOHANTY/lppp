import { useState, useEffect, useRef, useCallback } from 'react'
import { createCancelToken, AxiosRequestConfig } from '../services/api'

interface UseFetchState<T> {
  data: T | null
  loading: boolean
  error: string | null
}

export function useFetch<T>(url: string, config?: AxiosRequestConfig) {
  const [state, setState] = useState<UseFetchState<T>>({ data: null, loading: true, error: null })
  const cancelSourceRef = useRef(createCancelToken())

  const fetchData = useCallback(async () => {
    cancelSourceRef.current = createCancelToken()
    setState(prev => ({ ...prev, loading: true, error: null }))

    try {
      const response = await fetch(url, {
        ...config,
        headers: { 'Content-Type': 'application/json', ...config?.headers },
        signal: cancelSourceRef.current.token
      })
      if (!response.ok) throw new Error(`HTTP ${response.status}`)
      const data = await response.json()
      setState({ data, loading: false, error: null })
    } catch (err) {
      if (axios.isCancel(err)) return
      setState({ data: null, loading: false, error: err instanceof Error ? err.message : 'Unknown error' })
    }
  }, [url, config?.method])

  useEffect(() => {
    fetchData()
    return () => cancelSourceRef.current.cancel()
  }, [fetchData])

  return { ...state, refetch: fetchData }
}

import axios from 'axios'

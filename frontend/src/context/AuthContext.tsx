import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'
import api from '../services/api'

type AuthContextValue = {
  token: string | null
  login: (token: string) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('auth_token'))

  useEffect(() => {
    if (token) localStorage.setItem('auth_token', token)
    else localStorage.removeItem('auth_token')
  }, [token])

  // attach to axios
  useEffect(() => {
    const id = api.interceptors.request.use((config) => {
      if (token) {
        config.headers.set('Authorization', `Bearer ${token}`)
      }
      return config
    })
    return () => {
      api.interceptors.request.eject(id)
    }
  }, [token])

  const value = useMemo(
    () => ({ token, login: setToken, logout: () => setToken(null) }),
    [token]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}



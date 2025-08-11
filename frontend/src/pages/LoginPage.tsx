import { useEffect, useRef, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const googleDivRef = useRef<HTMLDivElement>(null)

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    const params = new URLSearchParams()
    params.set('username', email)
    params.set('password', password)
    const res = await api.post('/auth/login', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
    login(res.data.access_token)
    navigate('/generator')
  }

  // Google Identity Services
  useEffect(() => {
    const cb = (resp: any) => {
      api
        .post('/auth/google', { id_token: resp.credential })
        .then((r) => {
          login(r.data.access_token)
          navigate('/generator')
        })
    }
    const win = window as any
    if (!win.google) {
      const s = document.createElement('script')
      s.src = 'https://accounts.google.com/gsi/client'
      s.async = true
      s.defer = true
      s.onload = () => {
        win.google.accounts.id.initialize({ client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID, callback: cb })
        if (googleDivRef.current) win.google.accounts.id.renderButton(googleDivRef.current, { theme: 'outline', size: 'large' })
      }
      document.body.appendChild(s)
    } else {
      win.google.accounts.id.initialize({ client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID, callback: cb })
      if (googleDivRef.current) win.google.accounts.id.renderButton(googleDivRef.current, { theme: 'outline', size: 'large' })
    }
  }, [login, navigate])

  return (
    <div className="max-w-md mx-auto p-6">
      <h1 className="text-2xl font-semibold mb-4">Sign in</h1>
      <form onSubmit={onSubmit} className="space-y-3">
        <input className="w-full border px-3 py-2 rounded" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="w-full border px-3 py-2 rounded" placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button className="w-full bg-black text-white py-2 rounded" type="submit">Login</button>
      </form>
      <div className="mt-6 flex items-center"><div className="flex-1 h-px bg-gray-200" /><span className="px-3 text-gray-500">or</span><div className="flex-1 h-px bg-gray-200" /></div>
      <div ref={googleDivRef} className="mt-4 flex justify-center" />
    </div>
  )
}



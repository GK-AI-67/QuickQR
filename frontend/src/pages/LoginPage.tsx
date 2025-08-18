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
    console.log('Google client ID:', import.meta.env.VITE_GOOGLE_CLIENT_ID)
    
    const cb = (resp: any) => {
      console.log('Google login callback triggered', resp)
      api
        .post('/auth/google', { id_token: resp.credential })
        .then((r: any) => {
          console.log('Google login successful', r.data)
          login(r.data.access_token)
          console.log('Navigating to generator...')
          setTimeout(() => {
            navigate('/generator')
          }, 100)
        })
        .catch((error: any) => {
          console.error('Google login failed:', error)
        })
    }
    const win = window as any
    if (!win.google) {
      const s = document.createElement('script')
      s.src = 'https://accounts.google.com/gsi/client'
      s.async = true
      s.defer = true
      s.onload = () => {
        console.log('Google script loaded, initializing...')
        try {
          win.google.accounts.id.initialize({ 
            client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID, 
            callback: cb 
          })
          if (googleDivRef.current) {
            win.google.accounts.id.renderButton(googleDivRef.current, { theme: 'outline', size: 'large' })
            console.log('Google button rendered')
          }
        } catch (error) {
          console.error('Error initializing Google:', error)
        }
      }
      s.onerror = () => {
        console.error('Failed to load Google script')
      }
      document.body.appendChild(s)
    } else {
      console.log('Google already loaded, initializing...')
      try {
        win.google.accounts.id.initialize({ 
          client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID, 
          callback: cb 
        })
        if (googleDivRef.current) {
          win.google.accounts.id.renderButton(googleDivRef.current, { theme: 'outline', size: 'large' })
          console.log('Google button rendered')
        }
      } catch (error) {
        console.error('Error initializing Google:', error)
      }
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
      <button 
        onClick={() => {
          console.log('Test navigation button clicked')
          navigate('/generator')
        }}
        className="mt-4 w-full bg-blue-500 text-white py-2 rounded"
      >
        Test Navigation to Generator
      </button>
      <button 
        onClick={() => {
          console.log('Environment check:')
          console.log('VITE_API_URL:', import.meta.env.VITE_API_URL)
          console.log('VITE_GOOGLE_CLIENT_ID:', import.meta.env.VITE_GOOGLE_CLIENT_ID)
        }}
        className="mt-2 w-full bg-green-500 text-white py-2 rounded"
      >
        Check Environment Variables
      </button>
    </div>
  )
}



import { useState } from 'react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'
import { QrCode, Download } from 'lucide-react'

const NameQRPage = () => {
  const [name, setName] = useState('')
  const [qrCodeData, setQrCodeData] = useState<string | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)

  const generate = async () => {
    const content = name.trim()
    if (!content) {
      toast.error('Please enter a name')
      return
    }

    setIsGenerating(true)
    try {
      const API_BASE = import.meta.env.VITE_API_URL || 'https://quickqr-backend.onrender.com/api/v1'
      const token = localStorage.getItem('auth_token')
      const res = await fetch(`${API_BASE}/qr/generate`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          ...(token && { 'Authorization': `Bearer ${token}` })
        },
        body: JSON.stringify({
          content,
          qr_type: 'text',
          size: 512,
          error_correction: 'M',
          border: 4,
          foreground_color: '#000000',
          background_color: '#FFFFFF'
        })
      })
      const data = await res.json()
      if (data.success && data.qr_code_data) {
        setQrCodeData(data.qr_code_data)
        toast.success('QR generated!')
      } else {
        toast.error(data.error || 'Failed to generate QR')
      }
    } catch (e: any) {
      toast.error(e?.message || 'Failed to generate QR')
    } finally {
      setIsGenerating(false)
    }
  }

  const download = () => {
    if (!qrCodeData) return
    const link = document.createElement('a')
    link.href = qrCodeData
    link.download = `${name || 'name'}-qr.png`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-8"
        >
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
            Name QR
          </h1>
          <p className="text-gray-600">Generate a QR from just a name.</p>
        </motion.div>

        <div className="card p-6 space-y-4">
          <label className="block text-sm font-medium text-gray-700">Name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter a name"
            className="input"
          />

          <button
            onClick={generate}
            disabled={isGenerating}
            className="btn-primary w-full flex items-center justify-center"
          >
            {isGenerating ? 'Generating...' : (
              <>
                <QrCode className="w-4 h-4 mr-2" /> Generate
              </>
            )}
          </button>
        </div>

        <div className="card p-6 mt-6 text-center">
          {qrCodeData ? (
            <>
              <img src={qrCodeData} alt="Name QR" className="mx-auto w-64 h-64 object-contain" />
              <button onClick={download} className="btn-secondary mt-4 inline-flex items-center">
                <Download className="w-4 h-4 mr-2" /> Download PNG
              </button>
            </>
          ) : (
            <div className="text-gray-500">No QR yet</div>
          )}
        </div>
      </div>
    </div>
  )
}

export default NameQRPage



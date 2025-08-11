import { useState } from 'react'
import { motion } from 'framer-motion'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { 
  QrCode, 
  Download, 
  Copy, 
  Sparkles, 
  Settings, 
  RefreshCw,
  CheckCircle
} from 'lucide-react'
import { QRCodeRequest, AISuggestionResponse } from '../types'
import { qrCodeAPI, aiAPI } from '../services/api'
import QRCodeForm from '../components/QRCodeForm'
import QRCodePreview from '../components/QRCodePreview'
import AISuggestions from '../components/AISuggestions'
import ColorPicker from '../components/ColorPicker'

const GeneratorPage = () => {
  const [qrCodeData, setQrCodeData] = useState<string | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [aiSuggestions, setAiSuggestions] = useState<AISuggestionResponse | null>(null)
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [selectedColors, setSelectedColors] = useState({
    foreground: '#000000',
    background: '#FFFFFF'
  })

  const {
    register,
    watch,
    setValue,
    formState: { errors }
  } = useForm<QRCodeRequest>({
    defaultValues: {
      content: '',
      qr_type: 'url',
      size: 10,
      error_correction: 'M',
      border: 4,
      foreground_color: '#000000',
      background_color: '#FFFFFF'
    }
  })

  const watchedContent = watch('content')
  const watchedType = watch('qr_type')

  // Generate QR code
  const onSubmit = async (data: QRCodeRequest) => {
    if (!data.content.trim()) {
      toast.error('Please enter some content for your QR code')
      return
    }

    setIsGenerating(true)
    try {
      const response = await qrCodeAPI.generateQR({
        ...data,
        foreground_color: selectedColors.foreground,
        background_color: selectedColors.background
      })

      if (response.success && response.qr_code_data) {
        setQrCodeData(response.qr_code_data)
        toast.success('QR code generated successfully!')
      } else {
        toast.error(response.error || 'Failed to generate QR code')
      }
    } catch (error: any) {
      toast.error(error.message || 'Failed to generate QR code')
    } finally {
      setIsGenerating(false)
    }
  }

  // Generate QR code with file upload
  const onSubmitWithFile = async (formData: FormData) => {
    setIsGenerating(true)
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'https://quickqr-backend.onrender.com/api/v1'}/qr/generate-with-image`, {
        method: 'POST',
        body: formData
      })

      const data = await response.json()

      if (data.success && data.qr_code_data) {
        setQrCodeData(data.qr_code_data)
        toast.success('QR code generated successfully!')
      } else {
        toast.error(data.error || 'Failed to generate QR code')
      }
    } catch (error: any) {
      toast.error(error.message || 'Failed to generate QR code')
    } finally {
      setIsGenerating(false)
    }
  }

  // Get AI suggestions
  const getAISuggestions = async () => {
    if (!watchedContent.trim()) {
      toast.error('Please enter some content first')
      return
    }

    try {
      const response = await aiAPI.getSuggestions({
        content: watchedContent,
        qr_type: watchedType
      })
      setAiSuggestions(response)
      toast.success('AI suggestions loaded!')
    } catch (error: any) {
      toast.error(error.message || 'Failed to get AI suggestions')
    }
  }

  // Apply AI suggestion
  const applySuggestion = (suggestion: string) => {
    setValue('content', suggestion)
    toast.success('Suggestion applied!')
  }

  // Download QR code
  const downloadQRCode = () => {
    if (!qrCodeData) return

    const link = document.createElement('a')
    link.href = qrCodeData
    link.download = 'quickqr-code.png'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    toast.success('QR code downloaded!')
  }

  // Copy QR code data
  const copyQRCodeData = () => {
    if (!qrCodeData) return

    navigator.clipboard.writeText(qrCodeData)
    toast.success('QR code data copied to clipboard!')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-8"
        >
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            QR Code Generator
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Create beautiful, customizable QR codes with AI-powered suggestions and real-time preview.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Section */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="space-y-6"
          >
            {/* Main Form */}
            <div className="card p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <QrCode className="w-5 h-5 mr-2" />
                Generate QR Code
              </h2>
              
                             <QRCodeForm
                 register={register}
                 errors={errors}
                 onSubmit={onSubmit}
                 onSubmitWithFile={onSubmitWithFile}
                 isGenerating={isGenerating}
                 watch={watch}
               />
            </div>

            {/* AI Suggestions */}
            <div className="card p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                  <Sparkles className="w-5 h-5 mr-2" />
                  AI Suggestions
                </h3>
                <button
                  onClick={getAISuggestions}
                  disabled={!watchedContent.trim()}
                  className="btn-ghost text-sm"
                >
                  <RefreshCw className="w-4 h-4 mr-1" />
                  Refresh
                </button>
              </div>
              
              <AISuggestions
                suggestions={aiSuggestions}
                onApplySuggestion={applySuggestion}
              />
            </div>

            {/* Advanced Options */}
            <div className="card p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                  <Settings className="w-5 h-5 mr-2" />
                  Advanced Options
                </h3>
                <button
                  onClick={() => setShowAdvanced(!showAdvanced)}
                  className="btn-ghost text-sm"
                >
                  {showAdvanced ? 'Hide' : 'Show'}
                </button>
              </div>

              {showAdvanced && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="space-y-4"
                >
                  {/* Color Customization */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Colors
                    </label>
                    <ColorPicker
                      foreground={selectedColors.foreground}
                      background={selectedColors.background}
                      onChange={setSelectedColors}
                    />
                  </div>

                  {/* Size and Error Correction */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Size
                      </label>
                      <select
                        {...register('size')}
                        className="input"
                      >
                        <option value={8}>Small (8)</option>
                        <option value={10}>Medium (10)</option>
                        <option value={12}>Large (12)</option>
                        <option value={16}>Extra Large (16)</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Error Correction
                      </label>
                      <select
                        {...register('error_correction')}
                        className="input"
                      >
                        <option value="L">Low (7%)</option>
                        <option value="M">Medium (15%)</option>
                        <option value="Q">Quartile (25%)</option>
                        <option value="H">High (30%)</option>
                      </select>
                    </div>
                  </div>
                </motion.div>
              )}
            </div>
          </motion.div>

          {/* Preview Section */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="space-y-6"
          >
            {/* QR Code Preview */}
            <div className="card p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <QrCode className="w-5 h-5 mr-2" />
                Preview
              </h2>
              
              <QRCodePreview
                qrCodeData={qrCodeData}
                isGenerating={isGenerating}
              />

              {/* Action Buttons */}
              {qrCodeData && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex flex-col sm:flex-row gap-3 mt-6"
                >
                  <button
                    onClick={downloadQRCode}
                    className="btn-primary flex-1 flex items-center justify-center"
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Download PNG
                  </button>
                  <button
                    onClick={copyQRCodeData}
                    className="btn-secondary flex-1 flex items-center justify-center"
                  >
                    <Copy className="w-4 h-4 mr-2" />
                    Copy Data
                  </button>
                </motion.div>
              )}
            </div>

            {/* Tips Section */}
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <CheckCircle className="w-5 h-5 mr-2" />
                Tips for Best Results
              </h3>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-start">
                  <CheckCircle className="w-4 h-4 text-success-500 mr-2 mt-0.5 flex-shrink-0" />
                  Keep URLs short and memorable for better scanning
                </li>
                <li className="flex items-start">
                  <CheckCircle className="w-4 h-4 text-success-500 mr-2 mt-0.5 flex-shrink-0" />
                  Use high contrast colors for better readability
                </li>
                <li className="flex items-start">
                  <CheckCircle className="w-4 h-4 text-success-500 mr-2 mt-0.5 flex-shrink-0" />
                  Test your QR code before printing or sharing
                </li>
                <li className="flex items-start">
                  <CheckCircle className="w-4 h-4 text-success-500 mr-2 mt-0.5 flex-shrink-0" />
                  Use higher error correction for smaller QR codes
                </li>
              </ul>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default GeneratorPage 
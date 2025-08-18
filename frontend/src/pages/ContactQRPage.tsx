import { useState } from 'react'
import { motion } from 'framer-motion'
import { useForm } from 'react-hook-form'
import toast from 'react-hot-toast'
import { 
  QrCode, 
  Download, 
  Share2, 
  User, 
  Eye,
  EyeOff,
  Settings,
  CheckCircle
} from 'lucide-react'
import { ContactQRRequest, ContactField } from '../types'
import { contactQRAPI } from '../services/api'
import ColorPicker from '../components/ColorPicker'

const ContactQRPage = () => {
  const [qrCodeData, setQrCodeData] = useState<string | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [selectedColors, setSelectedColors] = useState({
    foreground: '#000000',
    background: '#FFFFFF'
  })

  const {
    register,
    watch,
    setValue,
    handleSubmit,
    formState: { errors }
  } = useForm<ContactQRRequest>({
    defaultValues: {
      full_name: { value: '', show: true },
      phone_number: { value: '', show: true },
      address: { value: '', show: true },
      email: { value: '', show: false },
      company: { value: '', show: false },
      website: { value: '', show: false },
      send_location_on_scan: true,
      size: 10,
      error_correction: 'M',
      border: 4,
      foreground_color: '#000000',
      background_color: '#FFFFFF'
    }
  })

  const watchedValues = watch()

  // Toggle field visibility
  const toggleFieldVisibility = (fieldName: keyof ContactQRRequest) => {
    if (fieldName === 'full_name' || fieldName === 'phone_number' || fieldName === 'address') {
      return // Required fields cannot be hidden
    }
    
    const currentValue = watchedValues[fieldName] as ContactField
    if (currentValue) {
      setValue(fieldName as any, { ...currentValue, show: !currentValue.show })
    }
  }

  // Generate Contact QR code
  const onSubmit = async (data: ContactQRRequest) => {
    if (!data.full_name.value.trim()) {
      toast.error('Full name is required')
      return
    }
    if (!data.phone_number.value.trim()) {
      toast.error('Phone number is required')
      return
    }
    if (!data.address.value.trim()) {
      toast.error('Address is required')
      return
    }

    setIsGenerating(true)
    try {
      const response = await contactQRAPI.generateContactQR({
        ...data,
        foreground_color: selectedColors.foreground,
        background_color: selectedColors.background
      })

      if (response.success && response.qr_code_data) {
        setQrCodeData(response.qr_code_data)
        toast.success('Contact QR code generated successfully!')
      } else {
        toast.error(response.error || 'Failed to generate Contact QR code')
      }
    } catch (error: any) {
      toast.error(error.message || 'Failed to generate Contact QR code')
    } finally {
      setIsGenerating(false)
    }
  }

  // Download QR code
  const downloadQRCode = () => {
    if (!qrCodeData) return

    const link = document.createElement('a')
    link.href = qrCodeData
    link.download = 'contact-qr-code.png'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    toast.success('Contact QR code downloaded!')
  }

  // Share QR code
  const shareQRCode = async () => {
    if (!qrCodeData) return

    try {
      if (navigator.share) {
        await navigator.share({
          title: 'Contact QR Code',
          text: 'Check out my contact information!',
          url: qrCodeData
        })
        toast.success('QR code shared!')
      } else {
        // Fallback: copy to clipboard
        await navigator.clipboard.writeText(qrCodeData)
        toast.success('QR code data copied to clipboard!')
      }
    } catch (error) {
      toast.error('Failed to share QR code')
    }
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
            Lost & Found QR
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Create a Lost & Found QR with your contact details; optionally receive the scanner's location via SMS.
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
            {/* Contact Form */}
            <div className="card p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                <User className="w-5 h-5 mr-2" />
                Contact Information
              </h2>
              
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                {/* Required Fields */}
                <div className="space-y-4">
                  <h3 className="text-lg font-medium text-gray-700">Required Fields</h3>
                  
                  {/* Full Name */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Full Name *
                    </label>
                    <div className="flex">
                      <input
                        type="text"
                        {...register('full_name.value', { required: 'Full name is required' })}
                        className="input flex-1 rounded-r-none"
                        placeholder="Enter your full name"
                      />
                      <div className="flex items-center px-3 bg-gray-100 border border-l-0 border-gray-300 rounded-r-md">
                        <Eye className="w-4 h-4 text-green-600" />
                        <span className="ml-1 text-xs text-green-600">Always visible</span>
                      </div>
                    </div>
                    {errors.full_name?.value && (
                      <p className="text-red-500 text-sm mt-1">{errors.full_name.value.message}</p>
                    )}
                  </div>

                  {/* Phone Number */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Phone Number *
                    </label>
                    <div className="flex">
                      <input
                        type="tel"
                        {...register('phone_number.value', { required: 'Phone number is required' })}
                        className="input flex-1 rounded-r-none"
                        placeholder="Enter your phone number"
                      />
                      <div className="flex items-center px-3 bg-gray-100 border border-l-0 border-gray-300 rounded-r-md">
                        <Eye className="w-4 h-4 text-green-600" />
                        <span className="ml-1 text-xs text-green-600">Always visible</span>
                      </div>
                    </div>
                    {errors.phone_number?.value && (
                      <p className="text-red-500 text-sm mt-1">{errors.phone_number.value.message}</p>
                    )}
                  </div>

                  {/* Address */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Address *
                    </label>
                    <div className="flex">
                      <textarea
                        {...register('address.value', { required: 'Address is required' })}
                        className="input flex-1 rounded-r-none resize-none"
                        rows={2}
                        placeholder="Enter your address"
                      />
                      <div className="flex items-center px-3 bg-gray-100 border border-l-0 border-gray-300 rounded-r-md">
                        <Eye className="w-4 h-4 text-green-600" />
                        <span className="ml-1 text-xs text-green-600">Always visible</span>
                      </div>
                    </div>
                    {errors.address?.value && (
                      <p className="text-red-500 text-sm mt-1">{errors.address.value.message}</p>
                    )}
                  </div>
                </div>

                {/* Optional Fields */}
                <div className="space-y-4">
                  <h3 className="text-lg font-medium text-gray-700">Optional Fields</h3>
                  
                  {/* Email */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Email Address
                    </label>
                    <div className="flex">
                      <input
                        type="email"
                        {...register('email.value')}
                        className="input flex-1 rounded-r-none"
                        placeholder="Enter your email address"
                      />
                      <button
                        type="button"
                        onClick={() => toggleFieldVisibility('email')}
                        className={`px-3 border border-l-0 rounded-r-md transition-colors ${
                          watchedValues.email?.show 
                            ? 'bg-green-100 border-green-300 text-green-700' 
                            : 'bg-gray-100 border-gray-300 text-gray-500'
                        }`}
                      >
                        {watchedValues.email?.show ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>

                  {/* Company */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Company
                    </label>
                    <div className="flex">
                      <input
                        type="text"
                        {...register('company.value')}
                        className="input flex-1 rounded-r-none"
                        placeholder="Enter your company name"
                      />
                      <button
                        type="button"
                        onClick={() => toggleFieldVisibility('company')}
                        className={`px-3 border border-l-0 rounded-r-md transition-colors ${
                          watchedValues.company?.show 
                            ? 'bg-green-100 border-green-300 text-green-700' 
                            : 'bg-gray-100 border-gray-300 text-gray-500'
                        }`}
                      >
                        {watchedValues.company?.show ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>

                  {/* Website */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Website
                    </label>
                    <div className="flex">
                      <input
                        type="url"
                        {...register('website.value')}
                        className="input flex-1 rounded-r-none"
                        placeholder="Enter your website URL"
                      />
                      <button
                        type="button"
                        onClick={() => toggleFieldVisibility('website')}
                        className={`px-3 border border-l-0 rounded-r-md transition-colors ${
                          watchedValues.website?.show 
                            ? 'bg-green-100 border-green-300 text-green-700' 
                            : 'bg-gray-100 border-gray-300 text-gray-500'
                        }`}
                      >
                        {watchedValues.website?.show ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>
                </div>

                {/* Generate Button */}
                <button
                  type="submit"
                  disabled={isGenerating}
                  className="btn-primary w-full flex items-center justify-center"
                >
                  {isGenerating ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Generating...
                    </>
                  ) : (
                    <>
                      <QrCode className="w-4 h-4 mr-2" />
                      Generate Contact QR
                    </>
                  )}
                </button>
              </form>
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
                  {/* Location Notification */}
                  <div className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <p className="text-sm font-medium text-gray-800">Send scanner location to my phone</p>
                      <p className="text-xs text-gray-500">Ask for device location once and SMS a Google Maps link to your phone when this QR is scanned.</p>
                    </div>
                    <input type="checkbox" {...register('send_location_on_scan')} className="h-5 w-5" />
                  </div>
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
              
              {qrCodeData ? (
                <div className="text-center">
                  <img 
                    src={qrCodeData} 
                    alt="Contact QR Code" 
                    className="mx-auto max-w-full h-auto rounded-lg shadow-lg"
                  />
                  
                  {/* Action Buttons */}
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
                      onClick={shareQRCode}
                      className="btn-secondary flex-1 flex items-center justify-center"
                    >
                      <Share2 className="w-4 h-4 mr-2" />
                      Share QR
                    </button>
                  </motion.div>
                </div>
              ) : (
                <div className="text-center py-12">
                  <QrCode className="w-24 h-24 text-gray-300 mx-auto mb-4" />
                  <p className="text-gray-500">Generate a Contact QR code to see the preview</p>
                </div>
              )}
            </div>

            {/* Privacy Info */}
            <div className="card p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <CheckCircle className="w-5 h-5 mr-2" />
                Privacy & Control
              </h3>
              <div className="space-y-3 text-sm text-gray-600">
                <div className="flex items-start">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                  <span>Only visible fields will appear when the QR code is scanned</span>
                </div>
                <div className="flex items-start">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                  <span>Required fields (name, phone, address) are always visible</span>
                </div>
                <div className="flex items-start">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                  <span>Optional fields can be hidden for privacy</span>
                </div>
                <div className="flex items-start">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                  <span>Generated QR codes are stored securely</span>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default ContactQRPage

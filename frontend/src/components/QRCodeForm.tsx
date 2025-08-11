import { useState, useRef } from 'react'
import { UseFormRegister, FieldErrors } from 'react-hook-form'
import { QRCodeRequest, QRCodeType } from '../types'
import { Globe, FileText, User, Wifi, Mail, Phone, MessageSquare, Upload, X } from 'lucide-react'

interface QRCodeFormProps {
  register: UseFormRegister<QRCodeRequest>
  errors: FieldErrors<QRCodeRequest>
  onSubmit: (data: QRCodeRequest) => void
  onSubmitWithFile?: (formData: FormData) => void
  isGenerating: boolean
  watch: any
}

const QRCodeForm = ({ register, errors, onSubmit, onSubmitWithFile, isGenerating, watch }: QRCodeFormProps) => {
  const [qrType, setQrType] = useState<QRCodeRequest['qr_type']>('url')
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)
  const content = watch('content')

  const qrTypeOptions = [
    { value: 'url', label: 'URL', icon: Globe, description: 'Website links' },
    { value: 'text', label: 'Text', icon: FileText, description: 'Plain text content' },
    { value: 'content', label: 'Content', icon: FileText, description: 'Display content when scanned' },
    { value: 'contact', label: 'Contact', icon: User, description: 'Contact information' },
    { value: 'wifi', label: 'WiFi', icon: Wifi, description: 'Network credentials' },
    { value: 'email', label: 'Email', icon: Mail, description: 'Email address' },
    { value: 'phone', label: 'Phone', icon: Phone, description: 'Phone number' },
    { value: 'sms', label: 'SMS', icon: MessageSquare, description: 'Text message' }
  ]

  const getPlaceholder = (type: string) => {
    switch (type) {
      case 'url':
        return 'https://example.com'
      case 'text':
        return 'Enter your text here...'
      case 'contact':
        return 'John Doe, john@example.com, +1234567890'
      case 'wifi':
        return 'NetworkName, Password, WPA'
      case 'email':
        return 'john@example.com'
      case 'phone':
        return '+1234567890'
      case 'sms':
        return '+1234567890:Your message here'
      default:
        return 'Enter content...'
    }
  }

  return (
    <form onSubmit={(e) => e.preventDefault()}>
      {/* QR Type Selection */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-3">
          QR Code Type
        </label>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
          {qrTypeOptions.map((option) => {
            const Icon = option.icon
            return (
              <button
                key={option.value}
                type="button"
                onClick={() => setQrType(option.value as QRCodeType)}
                className={`p-3 rounded-lg border-2 transition-all duration-200 text-left ${
                  qrType === option.value
                    ? 'border-primary-500 bg-primary-50 text-primary-700'
                    : 'border-gray-200 hover:border-gray-300 bg-white'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <Icon className="w-4 h-4" />
                  <span className="text-sm font-medium">{option.label}</span>
                </div>
                <p className="text-xs text-gray-500 mt-1">{option.description}</p>
              </button>
            )
          })}
        </div>
        <input
          type="hidden"
          {...register('qr_type')}
          value={qrType}
        />
      </div>

      {/* Title and Description for Content Type */}
      {qrType === 'content' && (
        <>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Title (Optional)
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter a title for your content..."
              className="input"
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Description (Optional)
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Enter a description..."
              className="input min-h-[80px] resize-none"
            />
          </div>
        </>
      )}

      {/* File Upload for Content Type */}
      {qrType === 'content' && (
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Upload Image (Optional)
          </label>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
            {selectedFile ? (
              <div className="space-y-2">
                <div className="flex items-center justify-center space-x-2">
                  <FileText className="w-5 h-5 text-primary-500" />
                  <span className="text-sm font-medium">{selectedFile.name}</span>
                  <button
                    type="button"
                    onClick={() => setSelectedFile(null)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
                <p className="text-xs text-gray-500">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            ) : (
              <div>
                <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                <p className="text-sm text-gray-600 mb-2">
                  Click to upload an image or drag and drop
                </p>
                <p className="text-xs text-gray-500">
                  PNG, JPG, GIF up to 5MB
                </p>
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="mt-2 btn-secondary text-sm"
                >
                  Choose File
                </button>
              </div>
            )}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={(e) => {
                const file = e.target.files?.[0]
                if (file && file.size <= 5 * 1024 * 1024) {
                  setSelectedFile(file)
                }
              }}
              className="hidden"
            />
          </div>
        </div>
      )}

      {/* Content Input */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          {qrType === 'content' ? 'Text Content (Optional if image uploaded)' : 'Content'}
        </label>
        <textarea
          {...register('content', { 
            required: qrType !== 'content' || (!selectedFile) ? 'Content is required' : false 
          })}
          placeholder={getPlaceholder(qrType)}
          className={`input min-h-[100px] resize-none ${
            errors.content ? 'border-error-500 focus:border-error-500 focus:ring-error-500' : ''
          }`}
        />
        {errors.content && (
          <p className="mt-1 text-sm text-error-600">{errors.content.message}</p>
        )}
      </div>

      {/* Generate Button */}
      <button
        type="submit"
        onClick={async (e) => {
          e.preventDefault()
          
          // For content type, validate that either content or file is provided
          if (qrType === 'content') {
            if (!content?.trim() && !selectedFile) {
              return
            }
          } else {
            if (!content || !content.trim()) {
              return
            }
          }
          
          // For content type with file, use the file upload endpoint
          if (qrType === 'content' && selectedFile) {
            const formData = new FormData()
            formData.append('content', content || '')
            formData.append('qr_type', qrType)
            formData.append('title', title)
            formData.append('description', description)
            formData.append('image_file', selectedFile)
            
            // Call a different function for file upload
            if (onSubmitWithFile) {
              onSubmitWithFile(formData)
              return
            }
          }
          
          // Regular submission
          onSubmit({ 
            content: content?.trim() || '', 
            qr_type: qrType, 
            size: 10, 
            error_correction: 'M', 
            border: 4, 
            foreground_color: '#000000', 
            background_color: '#FFFFFF',
            title: qrType === 'content' ? title : undefined,
            description: qrType === 'content' ? description : undefined
          })
        }}
        disabled={isGenerating}
        className="w-full btn-primary py-3 text-base font-medium"
      >
        {isGenerating ? (
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
            Generating...
          </div>
        ) : (
          <div className="flex items-center justify-center">
            <Globe className="w-5 h-5 mr-2" />
            Generate QR Code
          </div>
        )}
      </button>
    </form>
  )
}

export default QRCodeForm 
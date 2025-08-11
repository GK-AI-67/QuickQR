export interface QRCodeRequest {
  content: string
  qr_type: QRCodeType
  size: number
  error_correction: ErrorCorrectionLevel
  border: number
  foreground_color: string
  background_color: string
  logo_url?: string
  title?: string
  description?: string
}

export interface QRCodeResponse {
  success: boolean
  qr_code_data?: string
  qr_id?: string
  view_url?: string
  error?: string
  metadata?: QRCodeMetadata
}

export interface QRCodeMetadata {
  content: string
  qr_type: QRCodeType
  size: number
  error_correction: ErrorCorrectionLevel
}

export interface AISuggestionRequest {
  content: string
  qr_type: QRCodeType
  context?: string
}

export interface AISuggestionResponse {
  suggestions: string[]
  optimized_content?: string
  confidence_score: number
}

export type QRCodeType = 'url' | 'text' | 'contact' | 'wifi' | 'email' | 'phone' | 'sms' | 'content'

export type ErrorCorrectionLevel = 'L' | 'M' | 'Q' | 'H'

export interface QRCodeTypeOption {
  value: QRCodeType
  label: string
  description: string
  icon: string
}

export interface ErrorCorrectionOption {
  value: ErrorCorrectionLevel
  label: string
  description: string
}

export interface ContactInfo {
  name: string
  phone?: string
  email?: string
  company?: string
  title?: string
  address?: string
  website?: string
}

export interface WiFiInfo {
  ssid: string
  password: string
  encryption: 'WPA' | 'WEP' | 'nopass'
  hidden: boolean
}

export interface EmailInfo {
  email: string
  subject?: string
  body?: string
}

export interface SMSInfo {
  phone: string
  message: string
}

export interface ColorOption {
  name: string
  value: string
  bg: string
}

export interface SizeOption {
  value: number
  label: string
  description: string
}

export interface APIError {
  message: string
  status?: number
  details?: any
}

export interface QRContentDisplay {
  qr_id: string
  title?: string
  description?: string
  content: string
  content_type: string
  image_url?: string
  created_at: string
  qr_type: QRCodeType
} 
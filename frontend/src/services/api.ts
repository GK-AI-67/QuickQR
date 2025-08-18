import { QRCodeRequest, QRCodeResponse, AISuggestionRequest, AISuggestionResponse, ContactQRRequest, ContactQRResponse } from '../types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://quickqr-backend.onrender.com/api/v1'

// Helper function for API calls
async function apiCall<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('token')
  
  const config: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    },
    ...options,
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config)
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || errorData.message || `HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    if (error instanceof Error) {
      throw error
    }
    throw new Error('An unexpected error occurred')
  }
}

// QR Code API
export const qrCodeAPI = {
  generateQR: (data: QRCodeRequest): Promise<QRCodeResponse> =>
    apiCall<QRCodeResponse>('/qr/generate', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Get QR Code Types
  getTypes: async () => {
    const response = await fetch(`${API_BASE_URL}/qr/types`)
    return response.json()
  },

  // Get Error Correction Levels
  getErrorCorrectionLevels: async () => {
    const response = await fetch(`${API_BASE_URL}/qr/error-correction-levels`)
    return response.json()
  },

  // Validate URL
  validateURL: async (url: string) => {
    const response = await fetch(`${API_BASE_URL}/qr/validate-url`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    })
    return response.json()
  },
}

// AI API
export const aiAPI = {
  getSuggestions: (data: AISuggestionRequest): Promise<AISuggestionResponse> =>
    apiCall<AISuggestionResponse>('/ai/suggestions', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Analyze Content
  analyzeContent: async (content: string, qr_type: string) => {
    const response = await fetch(`${API_BASE_URL}/ai/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content, qr_type }),
    })
    return response.json()
  },

  // Generate Content
  generateContent: async (prompt: string, include_images: boolean = false) => {
    const response = await fetch(`${API_BASE_URL}/ai/generate-content`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt, include_images }),
    })
    return response.json()
  },

  // Check AI Health
  checkHealth: async () => {
    const response = await fetch(`${API_BASE_URL}/ai/health`)
    return response.json()
  },
}

// Contact QR API
export const contactQRAPI = {
  generateContactQR: (data: ContactQRRequest): Promise<ContactQRResponse> =>
    apiCall<ContactQRResponse>('/qr/generate-contact', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
}

export const contentAPI = {
  uploadPDF: async (file: File): Promise<{ path: string }> => {
    const form = new FormData()
    form.append('file', file)
    
    // Get auth token from localStorage
    const token = localStorage.getItem('auth_token')
    
    const response = await fetch(`${API_BASE_URL}/upload-pdf`, {
      method: 'POST',
      headers: { 
        'Content-Type': 'multipart/form-data',
        ...(token && { 'Authorization': `Bearer ${token}` }),
      },
      body: form,
    })
    return response.json()
  },
}

export const healthAPI = {
  // Check API Health
  checkHealth: async () => {
    const response = await fetch(`${API_BASE_URL}/health`)
    return response.json()
  },
} 
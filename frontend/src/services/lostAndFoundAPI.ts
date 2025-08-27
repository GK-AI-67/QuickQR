import api from './api'
import { apiLogger } from '../utils/logger'

// Use environment variable for API base URL
const API_BASE = '/lost-and-found'

export const lostAndFoundAPI = {
  async generateLostAndFoundQR(data: { name: string }) {
    const endpoint = `${API_BASE}/generate`
    const method = 'POST'
    
    try {
      apiLogger.logApiCall(endpoint, method, data, undefined, undefined, undefined, undefined)
      
      const res = await api.post(endpoint, data)
      
      apiLogger.logApiCall(endpoint, method, data, res.data, undefined, undefined, undefined)
      return res.data
    } catch (error: any) {
      apiLogger.logApiCall(endpoint, method, data, undefined, error, undefined, undefined)
      throw error
    }
  },
  
  async updateQRDetails(data: { 
    qr_id: string, 
    user_id: string,
    first_name: string, 
    last_name: string, 
    phone_number: string,
    email: string,
    address: string, 
    address_location: string,
    description: string,
    item_type: string,
    permissions?: Record<string, 'visible' | 'hidden'>,
    lock?: boolean
  }) {
    const endpoint = `${API_BASE}/update-details`
    const method = 'POST'
    
    try {
      apiLogger.logApiCall(endpoint, method, data, undefined, undefined, data.user_id, data.qr_id)
      
      const res = await api.post(endpoint, data)
      
      apiLogger.logApiCall(endpoint, method, data, res.data, undefined, data.user_id, data.qr_id)
      return res.data
    } catch (error: any) {
      apiLogger.logApiCall(endpoint, method, data, undefined, error, data.user_id, data.qr_id)
      throw error
    }
  },
  
  async getLostAndFoundQR(qr_id: string, user_id: string) {
    const endpoint = `${API_BASE}/${qr_id}?user_id=${user_id}`
    const method = 'GET'
    
    try {
      apiLogger.logApiCall(endpoint, method, { qr_id, user_id }, undefined, undefined, user_id, qr_id)
      
      const res = await api.get(endpoint)
      
      apiLogger.logApiCall(endpoint, method, { qr_id, user_id }, res.data, undefined, user_id, qr_id)
      return res.data
    } catch (error: any) {
      apiLogger.logApiCall(endpoint, method, { qr_id, user_id }, undefined, error, user_id, qr_id)
      throw error
    }
  },
  
  async markItemFound(data: { 
    qr_id: string, 
    user_id: string, 
    found_location: string, 
    found_date: string 
  }) {
    const endpoint = `${API_BASE}/mark-found`
    const method = 'POST'
    
    try {
      apiLogger.logApiCall(endpoint, method, data, undefined, undefined, data.user_id, data.qr_id)
      
      const res = await api.post(endpoint, data)
      
      apiLogger.logApiCall(endpoint, method, data, res.data, undefined, data.user_id, data.qr_id)
      return res.data
    } catch (error: any) {
      apiLogger.logApiCall(endpoint, method, data, undefined, error, data.user_id, data.qr_id)
      throw error
    }
  },
  
  async getUserQRs(user_id: string) {
    const endpoint = `${API_BASE}/user/${user_id}/qrs`
    const method = 'GET'
    
    try {
      apiLogger.logApiCall(endpoint, method, { user_id }, undefined, undefined, user_id, undefined)
      
      const res = await api.get(endpoint)
      
      apiLogger.logApiCall(endpoint, method, { user_id }, res.data, undefined, user_id, undefined)
      return res.data
    } catch (error: any) {
      apiLogger.logApiCall(endpoint, method, { user_id }, undefined, error, user_id, undefined)
      throw error
    }
  }
}

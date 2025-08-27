import React, { useState } from 'react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'
import { QrCode, Edit, Link2 } from 'lucide-react'
import { lostAndFoundAPI } from '../services/lostAndFoundAPI'
import { lostAndFoundLogger, uiLogger } from '../utils/logger'

const LostAndFoundQRPage = () => {
  const [name, setName] = useState('')
  const [qrCodeData, setQrCodeData] = useState<string | null>(null)
  const [qrApiLink, setQrApiLink] = useState<string | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [editDetails, setEditDetails] = useState({
    first_name: '',
    last_name: '',
    address: '',
    address_location: ''
  })

  // Log component mount
  React.useEffect(() => {
    uiLogger.info('COMPONENT_MOUNT', 'LostAndFoundQRPage component mounted')
    lostAndFoundLogger.info('PAGE_ACCESS', 'User accessed Lost and Found QR page')
    
    return () => {
      uiLogger.info('COMPONENT_UNMOUNT', 'LostAndFoundQRPage component unmounted')
    }
  }, [])

  // Generate QR by name
  const handleGenerateQR = async () => {
    if (!name.trim()) {
      uiLogger.warn('QR_GENERATION', 'Name is required for QR generation', { name })
      toast.error('Name is required')
      return
    }
    
    uiLogger.logUserAction('QR_GENERATION_START', 'User started QR generation', { name })
    setIsGenerating(true)
    
    try {
      lostAndFoundLogger.info('QR_GENERATION', 'Starting QR generation process', { name })
      
      const res = await lostAndFoundAPI.generateLostAndFoundQR({ name })
      
      if (res.success && res.qr_code_data) {
        setQrCodeData(res.qr_code_data)
        setQrApiLink(res.view_url)
        
        lostAndFoundLogger.info('QR_GENERATION_SUCCESS', 'QR generated successfully', { 
          name, 
          qr_id: res.qr_id,
          has_qr_data: !!res.qr_code_data,
          view_url: res.view_url 
        })
        
        uiLogger.logUserAction('QR_GENERATION_SUCCESS', 'QR generated successfully', { 
          name, 
          qr_id: res.qr_id 
        })
        
        toast.success('Lost & Found QR generated!')
      } else {
        lostAndFoundLogger.error('QR_GENERATION_FAILED', 'QR generation failed - no success response', { 
          name, 
          response: res 
        })
        
        uiLogger.logUserAction('QR_GENERATION_FAILED', 'QR generation failed', { 
          name, 
          error: res.error 
        })
        
        toast.error(res.error || 'Failed to generate Lost & Found QR')
      }
    } catch (error: any) {
      lostAndFoundLogger.error('QR_GENERATION_ERROR', 'QR generation threw exception', { 
        name, 
        error: error.message 
      }, error)
      
      uiLogger.logUserAction('QR_GENERATION_ERROR', 'QR generation error', { 
        name, 
        error: error.message 
      })
      
      toast.error(error.message || 'Failed to generate Lost & Found QR')
    } finally {
      setIsGenerating(false)
      uiLogger.logUserAction('QR_GENERATION_END', 'QR generation process ended', { name })
    }
  }

  // Edit QR details
  const handleEditDetails = async () => {
    if (!qrApiLink) {
      uiLogger.warn('EDIT_DETAILS', 'No QR API link available for editing', { qrApiLink })
      return
    }
    
    uiLogger.logUserAction('EDIT_DETAILS_START', 'User started editing QR details', { 
      qrApiLink,
      editDetails 
    })
    
    setIsEditing(true)
    
    try {
      // Extract QR ID from the API link
      const qrId = qrApiLink.split('/').pop()
      
      lostAndFoundLogger.info('EDIT_DETAILS', 'Starting QR details update', { 
        qrId,
        editDetails 
      })
      
      // Note: This would need to be updated to match the actual API structure
      // For now, we'll log the attempt but the actual API call needs proper parameters
      const res = await lostAndFoundAPI.updateQRDetails({
        qr_id: qrId || '',
        user_id: 'temp_user_id', // This should come from auth context
        first_name: editDetails.first_name,
        last_name: editDetails.last_name,
        phone_number: '',
        email: '',
        address: editDetails.address,
        address_location: editDetails.address_location,
        description: '',
        item_type: ''
      })
      
      if (res.success) {
        lostAndFoundLogger.info('EDIT_DETAILS_SUCCESS', 'QR details updated successfully', { 
          qrId,
          editDetails 
        })
        
        uiLogger.logUserAction('EDIT_DETAILS_SUCCESS', 'QR details updated successfully', { 
          qrId,
          editDetails 
        })
        
        toast.success('QR details updated!')
      } else {
        lostAndFoundLogger.error('EDIT_DETAILS_FAILED', 'QR details update failed', { 
          qrId,
          editDetails,
          response: res 
        })
        
        uiLogger.logUserAction('EDIT_DETAILS_FAILED', 'QR details update failed', { 
          qrId,
          error: res.error 
        })
        
        toast.error(res.error || 'Failed to update QR details')
      }
    } catch (error: any) {
      lostAndFoundLogger.error('EDIT_DETAILS_ERROR', 'QR details update threw exception', { 
        qrApiLink,
        editDetails,
        error: error.message 
      }, error)
      
      uiLogger.logUserAction('EDIT_DETAILS_ERROR', 'QR details update error', { 
        qrApiLink,
        error: error.message 
      })
      
      toast.error(error.message || 'Failed to update QR details')
    } finally {
      setIsEditing(false)
      uiLogger.logUserAction('EDIT_DETAILS_END', 'QR details editing process ended')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
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
            Generate a Lost & Found QR by name. Edit details after generation. Share or use the API link.
          </p>
        </motion.div>

        <div className="card p-6 space-y-6">
          <div className="flex flex-col sm:flex-row gap-4 items-center">
            <input
              type="text"
              value={name}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                const newName = e.target.value
                setName(newName)
                uiLogger.debug('NAME_INPUT_CHANGE', 'User changed name input', { 
                  newName, 
                  previousName: name 
                })
              }}
              className="input flex-1"
              placeholder="Enter a name to generate QR"
              disabled={isGenerating}
            />
            <button
              onClick={handleGenerateQR}
              disabled={isGenerating}
              className="btn-primary flex items-center justify-center"
            >
              {isGenerating ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Generating...
                </>
              ) : (
                <>
                  <QrCode className="w-4 h-4 mr-2" />
                  Generate QR
                </>
              )}
            </button>
          </div>

          {qrCodeData && (
            <div className="text-center mt-6">
              <img
                src={qrCodeData}
                alt="Lost & Found QR Code"
                className="mx-auto max-w-xs h-auto rounded-lg shadow-lg"
                onLoad={() => {
                  uiLogger.debug('QR_IMAGE_LOAD', 'QR code image loaded successfully')
                }}
                onError={(e) => {
                  uiLogger.error('QR_IMAGE_ERROR', 'QR code image failed to load', e)
                }}
              />
              {qrApiLink && (
                <div className="mt-4 flex flex-col items-center">
                  <a
                    href={qrApiLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 underline flex items-center"
                    onClick={() => {
                      uiLogger.logUserAction('API_LINK_CLICK', 'User clicked API link', { 
                        qrApiLink 
                      })
                    }}
                  >
                    <Link2 className="w-4 h-4 mr-1" />
                    API Link
                  </a>
                  <button
                    onClick={() => {
                      uiLogger.logUserAction('EDIT_BUTTON_CLICK', 'User clicked edit details button', { 
                        qrApiLink 
                      })
                      setIsEditing(true)
                    }}
                    className="btn-secondary mt-2 flex items-center"
                  >
                    <Edit className="w-4 h-4 mr-2" />
                    Edit Details
                  </button>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Edit Details Modal */}
        {isEditing && (
          <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-lg">
              <h2 className="text-xl font-semibold mb-4">Edit Lost & Found Details</h2>
              <div className="space-y-3">
                <input
                  type="text"
                  className="input w-full"
                  placeholder="First Name"
                  value={editDetails.first_name}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                    const newFirstName = e.target.value
                    setEditDetails({ ...editDetails, first_name: newFirstName })
                    uiLogger.debug('EDIT_FIRST_NAME_CHANGE', 'User changed first name in edit form', { 
                      newFirstName 
                    })
                  }}
                />
                <input
                  type="text"
                  className="input w-full"
                  placeholder="Last Name"
                  value={editDetails.last_name}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                    const newLastName = e.target.value
                    setEditDetails({ ...editDetails, last_name: newLastName })
                    uiLogger.debug('EDIT_LAST_NAME_CHANGE', 'User changed last name in edit form', { 
                      newLastName 
                    })
                  }}
                />
                <input
                  type="text"
                  className="input w-full"
                  placeholder="Address"
                  value={editDetails.address}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                    const newAddress = e.target.value
                    setEditDetails({ ...editDetails, address: newAddress })
                    uiLogger.debug('EDIT_ADDRESS_CHANGE', 'User changed address in edit form', { 
                      newAddress 
                    })
                  }}
                />
                <input
                  type="text"
                  className="input w-full"
                  placeholder="Address Location"
                  value={editDetails.address_location}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                    const newAddressLocation = e.target.value
                    setEditDetails({ ...editDetails, address_location: newAddressLocation })
                    uiLogger.debug('EDIT_ADDRESS_LOCATION_CHANGE', 'User changed address location in edit form', { 
                      newAddressLocation 
                    })
                  }}
                />
              </div>
              <div className="flex justify-end gap-2 mt-6">
                <button
                  onClick={() => {
                    uiLogger.logUserAction('EDIT_CANCEL_CLICK', 'User cancelled edit details', { 
                      editDetails 
                    })
                    setIsEditing(false)
                  }}
                  className="btn-ghost"
                >
                  Cancel
                </button>
                <button
                  onClick={handleEditDetails}
                  className="btn-primary"
                  disabled={isEditing}
                >
                  Save
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
      
      {/* Debug logs component - only visible in development */}
      <DebugLogs />
    </div>
  )
}

// Debug utility for development - can be removed in production
const DebugLogs = () => {
  const [showLogs, setShowLogs] = useState(false)
  const [logs, setLogs] = useState<any[]>([])

  const viewLogs = () => {
    const storedLogs = lostAndFoundLogger.getStoredLogs()
    setLogs(storedLogs)
    setShowLogs(true)
  }

  const clearLogs = () => {
    lostAndFoundLogger.clearStoredLogs()
    setLogs([])
    setShowLogs(false)
  }

  if (import.meta.env.DEV) {
    return (
      <div className="mt-8 p-4 bg-gray-100 rounded-lg">
        <h3 className="text-lg font-semibold mb-2">Debug Logs (Development Only)</h3>
        <div className="flex gap-2 mb-4">
          <button
            onClick={viewLogs}
            className="btn-secondary text-sm"
          >
            View Logs ({logs.length})
          </button>
          <button
            onClick={clearLogs}
            className="btn-ghost text-sm"
          >
            Clear Logs
          </button>
        </div>
        {showLogs && (
          <div className="max-h-60 overflow-y-auto bg-white p-2 rounded border">
            <pre className="text-xs">
              {logs.map((log, index) => (
                <div key={index} className="mb-1">
                  {JSON.stringify(log, null, 2)}
                </div>
              ))}
            </pre>
          </div>
        )}
      </div>
    )
  }

  return null
}

export default LostAndFoundQRPage

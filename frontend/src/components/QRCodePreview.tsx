import { motion } from 'framer-motion'
import { QrCode } from 'lucide-react'

interface QRCodePreviewProps {
  qrCodeData: string | null
  isGenerating: boolean
}

const QRCodePreview = ({ qrCodeData, isGenerating }: QRCodePreviewProps) => {
  if (isGenerating) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          className="w-16 h-16 border-4 border-primary-200 border-t-primary-600 rounded-full mb-4"
        />
        <p className="text-gray-600 font-medium">Generating QR Code...</p>
      </div>
    )
  }

  if (!qrCodeData) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-center">
        <div className="w-32 h-32 bg-gray-100 rounded-lg border-2 border-dashed border-gray-300 flex items-center justify-center mb-4">
          <QrCode className="w-12 h-12 text-gray-400" />
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">No QR Code Generated</h3>
        <p className="text-gray-600 max-w-sm">
          Enter your content and click "Generate QR Code" to see a preview here.
        </p>
      </div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      className="flex flex-col items-center"
    >
      <div className="bg-white p-4 rounded-lg shadow-medium mb-4">
        <img
          src={qrCodeData}
          alt="Generated QR Code"
          className="w-64 h-64 object-contain"
        />
      </div>
      
      <div className="text-center">
        <p className="text-sm text-gray-600">
          Scan this QR code with your mobile device
        </p>
      </div>
    </motion.div>
  )
}

export default QRCodePreview 
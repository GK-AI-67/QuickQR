import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  QrCode, 
  Sparkles, 
  Palette, 
  Download, 
  Zap, 
  Shield, 
  Smartphone,
  Globe,
  Users,
  Wifi
} from 'lucide-react'

const HomePage = () => {
  const features = [
    {
      icon: Sparkles,
      title: 'AI-Powered',
      description: 'Smart suggestions and content optimization using advanced AI technology.'
    },
    {
      icon: Palette,
      title: 'Customizable',
      description: 'Choose colors, add logos, and customize your QR codes to match your brand.'
    },
    {
      icon: Download,
      title: 'Multiple Formats',
      description: 'Export your QR codes in PNG, SVG, and PDF formats for any use case.'
    },
    {
      icon: Zap,
      title: 'Lightning Fast',
      description: 'Generate QR codes instantly with our optimized backend technology.'
    },
    {
      icon: Shield,
      title: 'Secure',
      description: 'Your data is protected with enterprise-grade security measures.'
    },
    {
      icon: Smartphone,
      title: 'Mobile Ready',
      description: 'Responsive design that works perfectly on all devices and screen sizes.'
    }
  ]

  const qrTypes = [
    { icon: Globe, name: 'URL', description: 'Website links' },
    { icon: QrCode, name: 'Text', description: 'Plain text content' },
    { icon: Users, name: 'Contact', description: 'Contact information' },
    { icon: Wifi, name: 'WiFi', description: 'Network credentials' }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-primary-50 via-white to-secondary-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                Generate Beautiful{' '}
                <span className="text-gradient">QR Codes</span>
                <br />
                with AI Intelligence
              </h1>
              <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                Create stunning, customizable QR codes with AI-powered suggestions. 
                Perfect for businesses, events, and personal use. Generate, customize, and download in seconds.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link
                  to="/generator"
                  className="btn-primary text-lg px-8 py-3 inline-flex items-center space-x-2"
                >
                  <QrCode className="w-5 h-5" />
                  <span>Start Generating</span>
                </Link>
                <button className="btn-secondary text-lg px-8 py-3">
                  Learn More
                </button>
              </div>
            </motion.div>
          </div>
        </div>

        {/* Floating QR Code Animation */}
        <motion.div
          animate={{ y: [-10, 10, -10] }}
          transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
          className="absolute top-1/4 right-10 hidden lg:block"
        >
          <div className="w-32 h-32 bg-white rounded-2xl shadow-large p-4">
            <div className="w-full h-full bg-gray-900 rounded-lg"></div>
          </div>
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose QuickQR?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Powerful features that make QR code generation simple, beautiful, and intelligent.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="card-hover p-6"
              >
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-primary-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* QR Types Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Multiple QR Code Types
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Generate different types of QR codes for various use cases and scenarios.
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {qrTypes.map((type, index) => (
              <motion.div
                key={type.name}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="card text-center p-6 hover:shadow-medium transition-shadow duration-200"
              >
                <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <type.icon className="w-8 h-8 text-primary-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {type.name}
                </h3>
                <p className="text-gray-600 text-sm">
                  {type.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-primary-600 to-primary-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
              Ready to Create Your QR Code?
            </h2>
            <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
              Join thousands of users who trust QuickQR for their QR code generation needs.
            </p>
            <Link
              to="/generator"
              className="bg-white text-primary-600 hover:bg-gray-100 px-8 py-3 rounded-lg font-semibold text-lg inline-flex items-center space-x-2 transition-colors duration-200"
            >
              <QrCode className="w-5 h-5" />
              <span>Get Started Now</span>
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

export default HomePage 
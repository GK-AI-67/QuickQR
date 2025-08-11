import { motion } from 'framer-motion'
import { 
  QrCode, 
  Sparkles, 
  Code, 
  Heart, 
  Users, 
  Shield,
  Zap,
  Palette,
  User,
  Mail,
  Phone
} from 'lucide-react'

const AboutPage = () => {
  const features = [
    {
      icon: Sparkles,
      title: 'AI-Powered',
      description: 'Advanced AI technology provides smart suggestions and content optimization for better QR codes.'
    },
    {
      icon: Palette,
      title: 'Customizable',
      description: 'Choose from multiple colors, sizes, and styles to match your brand and preferences.'
    },
    {
      icon: Zap,
      title: 'Lightning Fast',
      description: 'Generate QR codes instantly with our optimized backend and modern frontend technology.'
    },
    {
      icon: Shield,
      title: 'Secure',
      description: 'Your data is protected with enterprise-grade security and privacy measures.'
    },
    {
      icon: Users,
      title: 'User-Friendly',
      description: 'Intuitive interface designed for users of all technical levels and backgrounds.'
    },
    {
      icon: Code,
      title: 'Open Source',
      description: 'Built with modern technologies and available as open source for community contributions.'
    }
  ]

  const techStack = [
    { name: 'React 18', category: 'Frontend' },
    { name: 'TypeScript', category: 'Language' },
    { name: 'Tailwind CSS', category: 'Styling' },
    { name: 'FastAPI', category: 'Backend' },
    { name: 'Python', category: 'Language' },
    { name: 'QR Code Library', category: 'Core' },
    { name: 'OpenAI API', category: 'AI' },
    { name: 'Vite', category: 'Build Tool' }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            About QuickQR
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            A modern, AI-powered QR code generator designed to make creating beautiful and functional QR codes simple and efficient.
          </p>
        </motion.div>

        {/* Mission Section */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mb-16"
        >
          <div className="card p-8 text-center">
            <QrCode className="w-16 h-16 text-primary-600 mx-auto mb-6" />
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Our Mission</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              To provide the most user-friendly, feature-rich QR code generation experience with the power of artificial intelligence. 
              We believe that creating QR codes should be simple, beautiful, and intelligent.
            </p>
          </div>
        </motion.section>

        {/* Features Grid */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mb-16"
        >
          <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">
            Why Choose QuickQR?
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.6 + index * 0.1 }}
                className="card p-6 text-center"
              >
                <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                  <feature.icon className="w-6 h-6 text-primary-600" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Tech Stack */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="mb-16"
        >
          <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">
            Technology Stack
          </h2>
          <div className="card p-8">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {techStack.map((tech, index) => (
                <motion.div
                  key={tech.name}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.5, delay: 1 + index * 0.1 }}
                  className="text-center p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200"
                >
                  <p className="font-semibold text-gray-900">{tech.name}</p>
                  <p className="text-sm text-gray-500">{tech.category}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.section>

        {/* QR Code Types */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.2 }}
          className="mb-16"
        >
          <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">
            Supported QR Code Types
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { type: 'URL', description: 'Website links and web addresses' },
              { type: 'Text', description: 'Plain text content and messages' },
              { type: 'Contact', description: 'Contact information (vCard format)' },
              { type: 'WiFi', description: 'WiFi network credentials' },
              { type: 'Email', description: 'Email addresses with optional subject' },
              { type: 'Phone', description: 'Phone numbers for direct dialing' },
              { type: 'SMS', description: 'Text messages with pre-filled content' },
              { type: 'Custom', description: 'Custom data formats and content' }
            ].map((qrType, index) => (
              <motion.div
                key={qrType.type}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5, delay: 1.4 + index * 0.1 }}
                className="card p-4 text-center"
              >
                <h3 className="font-semibold text-gray-900 mb-2">{qrType.type}</h3>
                <p className="text-sm text-gray-600">{qrType.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.section>

        {/* Developer/Owner Information */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.6 }}
          className="mb-16"
        >
          <h2 className="text-2xl font-bold text-gray-900 text-center mb-8">
            Meet the Developer
          </h2>
          <div className="card p-8 max-w-2xl mx-auto">
            <div className="text-center mb-6">
              <div className="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <User className="w-10 h-10 text-primary-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Hardik Kothari</h3>
              <p className="text-gray-600">Full Stack Developer & Creator of QuickQR</p>
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center justify-center space-x-3">
                <Mail className="w-5 h-5 text-primary-600" />
                <a 
                  href="mailto:hardikkothari27@gmail.com" 
                  className="text-gray-700 hover:text-primary-600 transition-colors duration-200"
                >
                  hardikkothari27@gmail.com
                </a>
              </div>
              
              <div className="flex items-center justify-center space-x-3">
                <Phone className="w-5 h-5 text-primary-600" />
                <a 
                  href="tel:+919714022130" 
                  className="text-gray-700 hover:text-primary-600 transition-colors duration-200"
                >
                  +91 9714022130
                </a>
              </div>
            </div>
            
            <div className="mt-6 pt-6 border-t border-gray-200">
              <p className="text-gray-600 text-center">
                QuickQR is a passion project built with modern technologies to provide the best QR code generation experience. 
                Feel free to reach out for any questions, suggestions, or collaboration opportunities!
              </p>
            </div>
          </div>
        </motion.section>

        {/* Call to Action */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.8 }}
          className="text-center"
        >
          <div className="card p-8 bg-gradient-to-r from-primary-600 to-primary-700 text-white">
            <Heart className="w-12 h-12 mx-auto mb-4" />
            <h2 className="text-2xl font-bold mb-4">Made with ❤️ for the Community</h2>
            <p className="text-lg mb-6 max-w-2xl mx-auto">
              QuickQR is built with modern technologies and designed to be accessible to everyone. 
              We believe in the power of open source and community-driven development.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="btn-secondary bg-white text-primary-600 hover:bg-gray-100"
              >
                View on GitHub
              </a>
              <a
                href="/generator"
                className="btn-primary bg-white text-primary-600 hover:bg-gray-100"
              >
                Start Generating
              </a>
            </div>
          </div>
        </motion.section>
      </div>
    </div>
  )
}

export default AboutPage 
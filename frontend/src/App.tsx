import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import { useAuth } from './context/AuthContext'

function RequireAuth({ children }: { children: JSX.Element }) {
  const { token } = useAuth()
  const location = useLocation()
  if (!token) return <Navigate to="/login" state={{ from: location }} replace />
  return children
}
import { motion } from 'framer-motion'
import Header from './components/Header'
import Footer from './components/Footer'
import HomePage from './pages/HomePage'
import GeneratorPage from './pages/GeneratorPage'
import ContactQRPage from './pages/ContactQRPage'
import AboutPage from './pages/AboutPage'
import AIContentPage from './pages/AIContentPage'
import PDFDesignerPage from './pages/PDFDesignerPage'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <Header />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
            >
              <HomePage />
            </motion.div>
          } />
          <Route path="/login" element={
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <LoginPage />
            </motion.div>
          } />
          <Route path="/generator" element={
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <RequireAuth>
                <GeneratorPage />
              </RequireAuth>
            </motion.div>
          } />
          <Route path="/contact-qr" element={
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <RequireAuth>
                <ContactQRPage />
              </RequireAuth>
            </motion.div>
          } />
          <Route path="/lost-found" element={
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <RequireAuth>
                <ContactQRPage />
              </RequireAuth>
            </motion.div>
          } />
          <Route path="/ai-content" element={
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <AIContentPage />
            </motion.div>
          } />
          <Route path="/pdf-designer" element={
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <RequireAuth>
                <PDFDesignerPage />
              </RequireAuth>
            </motion.div>
          } />
          <Route path="/about" element={
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
            >
              <AboutPage />
            </motion.div>
          } />
          {/* Fallback: redirect unknown routes to login */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </main>
      <Footer />
    </div>
  )
}

export default App 
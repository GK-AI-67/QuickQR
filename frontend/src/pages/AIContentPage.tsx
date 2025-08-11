import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import api from '../services/api'

interface GeneratedContent {
  content: string
  images: string[]
  token_count: number
  prompt_length: number
}

export default function AIContentPage() {
  const { token } = useAuth()
  const [prompt, setPrompt] = useState('')
  const [includeImages, setIncludeImages] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedContent, setGeneratedContent] = useState<GeneratedContent | null>(null)
  const [error, setError] = useState('')
  const [showPDF, setShowPDF] = useState(false)

  const characterCount = prompt.length
  const maxCharacters = 2000

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt')
      return
    }

    if (characterCount > maxCharacters) {
      setError('Prompt exceeds 2000 character limit')
      return
    }

    setIsGenerating(true)
    setError('')
    setGeneratedContent(null)

    try {
      const response = await api.post('/ai/generate-content', {
        prompt: prompt.trim(),
        include_images: includeImages
      })

      setGeneratedContent(response.data)
      setShowPDF(true)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate content')
    } finally {
      setIsGenerating(false)
    }
  }

  const downloadPDF = () => {
    if (!generatedContent) return

    const content = `
      Generated Content
      ================
      
      Prompt: ${prompt}
      Token Count: ${generatedContent.token_count}
      Prompt Length: ${generatedContent.prompt_length}
      
      ${generatedContent.content}
      
      ${generatedContent.images.length > 0 ? '\nImages:\n' + generatedContent.images.join('\n') : ''}
    `

    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'generated-content.txt'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  if (!token) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">AI Content Generator</h1>
          <p className="text-gray-600">Please login to access the AI content generator.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">AI Content Generator</h1>
      
      {/* Input Section */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Generate Content</h2>
        
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Prompt (Max 2000 characters)
          </label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            className="w-full h-32 p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter your prompt here... (e.g., 'Write a comprehensive guide about sustainable gardening practices')"
            maxLength={maxCharacters}
          />
          <div className="flex justify-between items-center mt-2">
            <span className={`text-sm ${characterCount > maxCharacters ? 'text-red-500' : 'text-gray-500'}`}>
              {characterCount}/{maxCharacters} characters
            </span>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={includeImages}
                onChange={(e) => setIncludeImages(e.target.checked)}
                className="mr-2"
              />
              <span className="text-sm text-gray-700">Include AI-generated images</span>
            </label>
          </div>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        <button
          onClick={handleGenerate}
          disabled={isGenerating || characterCount > maxCharacters || !prompt.trim()}
          className="w-full bg-blue-600 text-white py-3 px-6 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {isGenerating ? 'Generating...' : 'Generate Content'}
        </button>
      </div>

      {/* Generated Content Section */}
      {generatedContent && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Generated Content</h2>
            <div className="space-x-2">
              <button
                onClick={() => setShowPDF(!showPDF)}
                className="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700"
              >
                {showPDF ? 'Hide' : 'Show'} PDF View
              </button>
              <button
                onClick={downloadPDF}
                className="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700"
              >
                Download
              </button>
            </div>
          </div>

          <div className="mb-4 text-sm text-gray-600">
            <p>Token Count: {generatedContent.token_count}</p>
            <p>Prompt Length: {generatedContent.prompt_length} characters</p>
          </div>

          {showPDF && (
            <div className="border border-gray-300 rounded-md p-6 bg-gray-50">
              <div className="prose max-w-none">
                <h3 className="text-lg font-semibold mb-4">Generated Content:</h3>
                <div className="whitespace-pre-wrap text-gray-800">
                  {generatedContent.content}
                </div>
                
                {generatedContent.images.length > 0 && (
                  <div className="mt-6">
                    <h4 className="text-md font-semibold mb-3">Generated Images:</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {generatedContent.images.map((imageUrl, index) => (
                        <div key={index} className="text-center">
                          <img
                            src={imageUrl}
                            alt={`Generated image ${index + 1}`}
                            className="max-w-full h-auto rounded-md shadow-md"
                          />
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

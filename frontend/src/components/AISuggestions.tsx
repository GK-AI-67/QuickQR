import { motion } from 'framer-motion'
import { Sparkles, CheckCircle, AlertCircle } from 'lucide-react'
import { AISuggestionResponse } from '../types'

interface AISuggestionsProps {
  suggestions: AISuggestionResponse | null
  onApplySuggestion: (suggestion: string) => void
}

const AISuggestions = ({ suggestions, onApplySuggestion }: AISuggestionsProps) => {
  if (!suggestions) {
    return (
      <div className="text-center py-6">
        <Sparkles className="w-8 h-8 text-gray-400 mx-auto mb-2" />
        <p className="text-sm text-gray-500">
          Enter some content and click "Refresh" to get AI suggestions
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Confidence Score */}
      <div className="flex items-center justify-between p-3 bg-primary-50 rounded-lg">
        <span className="text-sm font-medium text-primary-700">AI Confidence</span>
        <span className="text-sm font-semibold text-primary-700">
          {Math.round(suggestions.confidence_score * 100)}%
        </span>
      </div>

      {/* Optimized Content */}
      {suggestions.optimized_content && (
        <div className="p-3 bg-success-50 rounded-lg border border-success-200">
          <div className="flex items-start space-x-2">
            <CheckCircle className="w-4 h-4 text-success-600 mt-0.5 flex-shrink-0" />
            <div className="flex-1">
              <p className="text-sm font-medium text-success-800 mb-1">
                Optimized Content
              </p>
              <p className="text-sm text-success-700 bg-white p-2 rounded border">
                {suggestions.optimized_content}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Suggestions List */}
      {suggestions.suggestions.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-3">Suggestions</h4>
          <div className="space-y-2">
            {suggestions.suggestions.map((suggestion, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors duration-200"
              >
                <Sparkles className="w-4 h-4 text-primary-600 mt-0.5 flex-shrink-0" />
                <div className="flex-1">
                  <p className="text-sm text-gray-700">{suggestion}</p>
                </div>
                <button
                  onClick={() => onApplySuggestion(suggestion)}
                  className="btn-ghost text-xs px-2 py-1 hover:bg-primary-100 hover:text-primary-700"
                >
                  Apply
                </button>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* No Suggestions */}
      {suggestions.suggestions.length === 0 && (
        <div className="text-center py-4">
          <AlertCircle className="w-6 h-6 text-gray-400 mx-auto mb-2" />
          <p className="text-sm text-gray-500">
            No specific suggestions available for this content
          </p>
        </div>
      )}
    </div>
  )
}

export default AISuggestions 
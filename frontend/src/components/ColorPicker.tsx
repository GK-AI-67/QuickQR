import { HexColorPicker } from 'react-colorful'
import { useState } from 'react'
import { Palette } from 'lucide-react'

interface ColorPickerProps {
  foreground: string
  background: string
  onChange: (colors: { foreground: string; background: string }) => void
}

const ColorPicker = ({ foreground, background, onChange }: ColorPickerProps) => {
  const [activePicker, setActivePicker] = useState<'foreground' | 'background' | null>(null)

  const presetColors = [
    '#000000', '#FFFFFF', '#3B82F6', '#EF4444', '#10B981', '#F59E0B',
    '#8B5CF6', '#EC4899', '#06B6D4', '#84CC16', '#F97316', '#6366F1'
  ]

  const handleColorChange = (color: string) => {
    if (activePicker === 'foreground') {
      onChange({ foreground: color, background })
    } else if (activePicker === 'background') {
      onChange({ foreground, background: color })
    }
  }

  return (
    <div className="space-y-4">
      {/* Color Swatches */}
      <div className="flex space-x-4">
        {/* Foreground Color */}
        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Foreground Color
          </label>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setActivePicker(activePicker === 'foreground' ? null : 'foreground')}
              className="w-10 h-10 rounded-lg border-2 border-gray-300 overflow-hidden hover:border-primary-500 transition-colors duration-200"
              style={{ backgroundColor: foreground }}
            />
            <span className="text-sm font-mono text-gray-600">{foreground}</span>
          </div>
        </div>

        {/* Background Color */}
        <div className="flex-1">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Background Color
          </label>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setActivePicker(activePicker === 'background' ? null : 'background')}
              className="w-10 h-10 rounded-lg border-2 border-gray-300 overflow-hidden hover:border-primary-500 transition-colors duration-200"
              style={{ backgroundColor: background }}
            />
            <span className="text-sm font-mono text-gray-600">{background}</span>
          </div>
        </div>
      </div>

      {/* Color Picker */}
      {activePicker && (
        <div className="space-y-3">
          <div className="flex items-center space-x-2">
            <Palette className="w-4 h-4 text-gray-600" />
            <span className="text-sm font-medium text-gray-700">
              {activePicker === 'foreground' ? 'Foreground' : 'Background'} Color
            </span>
          </div>
          
          <div className="flex space-x-4">
            <HexColorPicker
              color={activePicker === 'foreground' ? foreground : background}
              onChange={handleColorChange}
              className="w-full max-w-[200px]"
            />
            
            {/* Preset Colors */}
            <div className="flex-1">
              <p className="text-sm font-medium text-gray-700 mb-2">Preset Colors</p>
              <div className="grid grid-cols-6 gap-2">
                {presetColors.map((color) => (
                  <button
                    key={color}
                    onClick={() => handleColorChange(color)}
                    className="w-8 h-8 rounded border-2 border-gray-300 hover:border-primary-500 transition-colors duration-200"
                    style={{ backgroundColor: color }}
                    title={color}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Preview */}
      <div className="p-3 bg-gray-50 rounded-lg">
        <p className="text-sm font-medium text-gray-700 mb-2">Preview</p>
        <div className="flex items-center space-x-4">
          <div className="w-16 h-16 bg-white rounded-lg border-2 border-gray-300 flex items-center justify-center">
            <div 
              className="w-12 h-12 rounded"
              style={{ 
                backgroundColor: background,
                border: `2px solid ${foreground}`
              }}
            />
          </div>
          <div className="text-sm text-gray-600">
            <p>Foreground: {foreground}</p>
            <p>Background: {background}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ColorPicker 
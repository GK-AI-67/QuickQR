import React, { useRef, useState } from 'react'
import html2canvas from 'html2canvas'
import { jsPDF } from 'jspdf'
import api, { aiAPI, contentAPI, qrCodeAPI } from '../services/api'
import type { QRCodeRequest, ErrorCorrectionLevel, QRCodeType } from '../types'

type DesignerTextBox = {
  id: string
  title: string
  prompt: string
  content: string
  isLoading: boolean
  error?: string
}

const A4_WIDTH_PX = 794 // ~210mm at ~96 DPI
const A4_HEIGHT_PX = 1123 // ~297mm at ~96 DPI

export default function PDFDesignerPage() {
  const previewRef = useRef<HTMLDivElement | null>(null)
  const [generatedQR, setGeneratedQR] = useState<string | null>(null)
  const [pdfUrl, setPdfUrl] = useState<string | null>(null)
  const [logoDataUrl, setLogoDataUrl] = useState<string | null>(null)
  const [logoUrlInput, setLogoUrlInput] = useState('')
  const [headerText, setHeaderText] = useState('')
  const [footerText, setFooterText] = useState('')
  const [boxes, setBoxes] = useState<DesignerTextBox[]>([
    { id: crypto.randomUUID(), title: 'Section 1', prompt: '', content: '', isLoading: false },
  ])
  const [isBuilding, setIsBuilding] = useState(false)

  const addBox = () => {
    setBoxes((prev: DesignerTextBox[]) => [
      ...prev,
      { id: crypto.randomUUID(), title: `Section ${prev.length + 1}`, prompt: '', content: '', isLoading: false },
    ])
  }

  const removeBox = (id: string) => {
    setBoxes((prev: DesignerTextBox[]) => prev.filter((b: DesignerTextBox) => b.id !== id))
  }

  const updateBox = (id: string, patch: Partial<DesignerTextBox>) => {
    setBoxes((prev: DesignerTextBox[]) => prev.map((b: DesignerTextBox) => (b.id === id ? { ...b, ...patch } : b)))
  }

  const onLogoFile = (file?: File) => {
    if (!file) return
    const reader = new FileReader()
    reader.onload = () => setLogoDataUrl(reader.result as string)
    reader.readAsDataURL(file)
  }

  const applyLogoUrl = () => setLogoDataUrl(logoUrlInput || null)

  const askAIForBox = async (id: string) => {
    const box: DesignerTextBox | undefined = boxes.find((b: DesignerTextBox) => b.id === id)
    if (!box) return
    if (!box.prompt.trim()) {
      updateBox(id, { error: 'Enter a prompt' })
      return
    }
    updateBox(id, { isLoading: true, error: undefined })
    try {
      const res = await aiAPI.generateContent(box.prompt, false)
      updateBox(id, { content: res.content || '', isLoading: false })
    } catch (e: any) {
      updateBox(id, { error: e?.message || 'AI failed', isLoading: false })
    }
  }

  const buildPdf = async (openInNewTab: boolean) => {
    if (!previewRef.current) return
    setIsBuilding(true)
    try {
      const canvas = await html2canvas(previewRef.current, { scale: 2, backgroundColor: '#ffffff' })
      const imgData = canvas.toDataURL('image/png')
      const pdf = new jsPDF('p', 'pt', 'a4')
      const pageWidth = pdf.internal.pageSize.getWidth()
      const pageHeight = pdf.internal.pageSize.getHeight()
      const ratio = Math.min(pageWidth / canvas.width, pageHeight / canvas.height)
      const imgWidth = canvas.width * ratio
      const imgHeight = canvas.height * ratio
      const x = (pageWidth - imgWidth) / 2
      const y = (pageHeight - imgHeight) / 2
      pdf.addImage(imgData, 'PNG', x, y, imgWidth, imgHeight)
      if (openInNewTab) {
        const blobUrl = pdf.output('bloburl')
        window.open(blobUrl, '_blank')
      } else {
        pdf.save('document.pdf')
      }
    } finally {
      setIsBuilding(false)
    }
  }

  const createQRForPdf = async () => {
    if (!previewRef.current) return
    setIsBuilding(true)
    try {
      // Render preview to PDF Blob
      const canvas = await html2canvas(previewRef.current, { scale: 2, backgroundColor: '#ffffff' })
      const pdf = new jsPDF('p', 'pt', 'a4')
      const pageWidth = pdf.internal.pageSize.getWidth()
      const pageHeight = pdf.internal.pageSize.getHeight()
      const ratio = Math.min(pageWidth / canvas.width, pageHeight / canvas.height)
      const imgWidth = canvas.width * ratio
      const imgHeight = canvas.height * ratio
      const x = (pageWidth - imgWidth) / 2
      const y = (pageHeight - imgHeight) / 2
      pdf.addImage(canvas.toDataURL('image/png'), 'PNG', x, y, imgWidth, imgHeight)
      const blob = pdf.output('blob') as Blob

      // Upload PDF to backend
      const file = new File([blob], 'designed.pdf', { type: 'application/pdf' })
      const { path } = await contentAPI.uploadPDF(file)
      const fullUrl = (api.defaults.baseURL ? api.defaults.baseURL.replace(/\/api\/v1$/, '') : window.location.origin) + path
      setPdfUrl(fullUrl)

      // Create QR pointing to the uploaded PDF
      const request: QRCodeRequest = {
        content: fullUrl,
        qr_type: 'url' as QRCodeType,
        size: 512,
        error_correction: 'M' as ErrorCorrectionLevel,
        border: 4,
        foreground_color: '#000000',
        background_color: '#FFFFFF',
      }
      const qr = await qrCodeAPI.generateQR(request)
      if (qr.qr_code_data) {
        setGeneratedQR(qr.qr_code_data)
      }
    } catch (e) {
      // no-op UI error toast in this minimal change
    } finally {
      setIsBuilding(false)
    }
  }

  const downloadQR = () => {
    if (!generatedQR) return
    const link = document.createElement('a')
    link.href = generatedQR
    link.download = 'pdf-qr-code.png'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">PDF Designer</h1>

      {/* Controls */}
      <div className="grid lg:grid-cols-3 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow p-4 space-y-4">
          <h2 className="font-semibold">Branding</h2>
          <div>
            <label className="block text-sm text-gray-600 mb-1">Header</label>
            <input value={headerText} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setHeaderText(e.target.value)} className="w-full border rounded px-3 py-2" placeholder="Header text" />
          </div>
          <div>
            <label className="block text-sm text-gray-600 mb-1">Footer</label>
            <input value={footerText} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFooterText(e.target.value)} className="w-full border rounded px-3 py-2" placeholder="Footer text" />
          </div>
          <div className="space-y-2">
            <label className="block text-sm text-gray-600">Logo</label>
            <input type="file" accept="image/*" onChange={(e) => onLogoFile(e.target.files?.[0] || undefined)} />
            <div className="flex gap-2 items-center">
              <input value={logoUrlInput} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setLogoUrlInput(e.target.value)} placeholder="Or paste logo URL" className="flex-1 border rounded px-3 py-2" />
              <button onClick={applyLogoUrl} className="px-3 py-2 border rounded">Use</button>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-4 space-y-3 lg:col-span-2">
          <div className="flex justify-between items-center">
            <h2 className="font-semibold">Text Boxes</h2>
            <button onClick={addBox} className="px-3 py-2 bg-blue-600 text-white rounded">Add Box</button>
          </div>

          {boxes.map((box: DesignerTextBox, idx: number) => (
            <div key={box.id} className="border rounded p-3">
              <div className="flex gap-2 mb-2">
                <input value={box.title} onChange={(e: React.ChangeEvent<HTMLInputElement>) => updateBox(box.id, { title: e.target.value })} className="flex-1 border rounded px-3 py-2" placeholder={`Title ${idx + 1}`} />
                <button onClick={() => removeBox(box.id)} className="px-3 py-2 border rounded text-red-600">Remove</button>
              </div>
              <div className="flex gap-2 mb-2">
                <input value={box.prompt} onChange={(e: React.ChangeEvent<HTMLInputElement>) => updateBox(box.id, { prompt: e.target.value })} className="flex-1 border rounded px-3 py-2" placeholder="Ask AI: describe what to generate" />
                <button onClick={() => askAIForBox(box.id)} disabled={box.isLoading} className="px-3 py-2 bg-green-600 text-white rounded disabled:opacity-50">
                  {box.isLoading ? 'Generating…' : 'Generate with AI'}
                </button>
              </div>
              {box.error && <div className="text-sm text-red-600 mb-2">{box.error}</div>}
              <textarea value={box.content} onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => updateBox(box.id, { content: e.target.value })} className="w-full h-28 border rounded px-3 py-2" placeholder="Content" />
            </div>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-3 mb-6">
        <button onClick={() => buildPdf(true)} disabled={isBuilding} className="px-4 py-2 bg-emerald-600 text-white rounded disabled:opacity-50">View PDF</button>
        <button onClick={() => buildPdf(false)} disabled={isBuilding} className="px-4 py-2 bg-purple-600 text-white rounded disabled:opacity-50">Download PDF</button>
        <button onClick={createQRForPdf} disabled={isBuilding} className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50">Create QR for PDF</button>
      </div>

      {/* Generated QR Code Section */}
      {generatedQR && (
        <div className="bg-white rounded-lg shadow p-4 mb-6">
          <h2 className="font-semibold mb-3">Generated QR Code</h2>
          <div className="flex flex-col md:flex-row gap-6 items-start">
            <div className="flex-shrink-0">
              <img src={generatedQR} alt="PDF QR Code" className="w-64 h-64 border rounded-lg shadow-md" />
            </div>
            <div className="flex-1 space-y-4">
              <div>
                <h3 className="font-medium text-gray-900 mb-2">QR Code Details</h3>
                <p className="text-sm text-gray-600 mb-2">This QR code links to your generated PDF document.</p>
                {pdfUrl && (
                  <div className="bg-gray-50 p-3 rounded border">
                    <p className="text-xs text-gray-500 mb-1">PDF URL:</p>
                    <p className="text-sm font-mono break-all">{pdfUrl}</p>
                  </div>
                )}
              </div>
              <div className="flex gap-3">
                <button onClick={downloadQR} className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">
                  Download QR Code
                </button>
                <a href={pdfUrl || '#'} target="_blank" rel="noopener noreferrer" className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
                  Open PDF
                </a>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Preview (scrollable container) */}
      <div className="bg-white rounded-lg shadow p-4">
        <h2 className="font-semibold mb-3">Preview</h2>
        <div className="overflow-auto" style={{ maxHeight: '75vh' }}>
          <div
            ref={previewRef}
            className="mx-auto border relative"
            style={{ width: A4_WIDTH_PX, height: A4_HEIGHT_PX, background: '#ffffff' }}
          >
            {/* Header */}
            <div className="flex items-center gap-3 px-8 pt-8">
              {logoDataUrl && (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={logoDataUrl} alt="Logo" className="h-48 w-48 object-contain" />
              )}
              <div className="text-3xl font-bold">{headerText}</div>
            </div>

            {/* Content */}
            <div className="px-8 mt-6 space-y-4 pb-40">
              {boxes.map((b: DesignerTextBox) => (
                <div key={b.id} className="border rounded p-4">
                  <div className="font-semibold mb-2">{b.title}</div>
                  <div className="whitespace-pre-wrap leading-6 text-gray-800">{b.content}</div>
                </div>
              ))}
            </div>

            {/* Footer */}
            <div className="absolute bottom-0 left-0 right-0 px-8 py-6 text-sm text-gray-600 border-t bg-white shadow-sm">
              {footerText}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}



import { useState } from 'react'

function App() {
  const [uploading, setUploading] = useState(false)
  const [uploadResult, setUploadResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileSelect = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    setUploadResult(null)
    setError(null)
    setUploading(true)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('/api/files/', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`)
      }

      const data = await response.json()
      setUploadResult(data)
      // Reset file input
      event.target.value = ''
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl p-8 max-w-md w-full">
        <h1 className="text-4xl font-bold text-center text-indigo-600 mb-6">
          Transmute
        </h1>
        <p className="text-gray-600 text-center mb-8">
          File conversion made simple
        </p>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {uploading ? 'Uploading...' : 'Select a file to upload'}
            </label>
            <input
              type="file"
              onChange={handleFileSelect}
              disabled={uploading}
              className="block w-full text-sm text-gray-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-lg file:border-0
                file:text-sm file:font-semibold
                file:bg-indigo-50 file:text-indigo-700
                hover:file:bg-indigo-100
                cursor-pointer
                disabled:opacity-50 disabled:cursor-not-allowed"
            />
          </div>

          {uploading && (
            <div className="text-sm text-indigo-600 font-medium">
              Uploading file...
            </div>
          )}

          {error && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {error}
            </div>
          )}

          {uploadResult && (
            <div className="p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
              <p className="font-semibold mb-1">Upload successful!</p>
              <p className="text-xs">File ID: {uploadResult.metadata?.id}</p>
              <p className="text-xs">Compatible Formats: {uploadResult.metadata?.compatible_formats?.join(', ')}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App

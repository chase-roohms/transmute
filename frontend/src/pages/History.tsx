import { useState, useEffect } from 'react'
import FileListItem, { FileInfo, ConversionInfo } from '../components/FileListItem'

interface FileRecord {
  id: string
  original_filename: string
  media_type: string
  extension: string
  size_bytes: number
  created_at: string
  conversion?: ConversionInfo
}

function History() {
  const [conversions, setConversions] = useState<FileRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [downloadingId, setDownloadingId] = useState<string | null>(null)
  const [deletingId, setDeletingId] = useState<string | null>(null)

  useEffect(() => {
    const fetchConversions = async () => {
      try {
        const response = await fetch('/api/conversions/complete')
        if (!response.ok) throw new Error('Failed to fetch conversions')
        const data = await response.json()
        setConversions(data.conversions)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load conversions')
      } finally {
        setLoading(false)
      }
    }
    fetchConversions()
  }, [])

  const handleDownload = async (conversion: ConversionInfo) => {
    setDownloadingId(conversion.id)
    try {
      const response = await fetch(`/api/files/${conversion.id}`)
      if (!response.ok) throw new Error('Download failed')

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url

      let filename = conversion.original_filename || 'download'
      const lastDotIndex = filename.lastIndexOf('.')
      if (lastDotIndex > 0) {
        filename = filename.substring(0, lastDotIndex)
      }
      filename += conversion.extension || ''

      a.download = filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Download failed')
    } finally {
      setDownloadingId(null)
    }
  }

  const handleDelete = async (fileId: string) => {
    setDeletingId(fileId)
    try {
      const response = await fetch(`/api/files/${fileId}`, { method: 'DELETE' })
      if (!response.ok) throw new Error('Delete failed')
      setConversions(prev => prev.filter(f => f.id !== fileId))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Delete failed')
    } finally {
      setDeletingId(null)
    }
  }

  const convertedFiles = conversions
    .filter(f => f.conversion)
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())

  return (
    <div className="min-h-screen bg-gradient-to-br from-surface-dark to-surface-light p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-primary mb-6">History</h1>

        {error && (
          <div className="p-3 bg-primary/20 border border-primary rounded-lg text-primary-light text-sm mb-4">
            {error}
          </div>
        )}

        {loading && (
          <p className="text-text-muted text-sm">Loading conversions...</p>
        )}

        {!loading && convertedFiles.length === 0 && (
          <p className="text-text-muted text-sm">No converted files yet.</p>
        )}

        {!loading && convertedFiles.length > 0 && (
          <div className="space-y-3">
            {convertedFiles.map(file => {
              const fileInfo: FileInfo = {
                id: file.id,
                original_filename: file.original_filename,
                media_type: file.media_type,
                extension: file.extension,
                size_bytes: file.size_bytes,
                created_at: file.created_at,
              }
              return (
                <FileListItem
                  key={file.id}
                  file={fileInfo}
                  conversion={file.conversion}
                  onDownload={() => handleDownload(file.conversion!)}
                  onDelete={() => handleDelete(file.id)}
                  isDeleting={deletingId === file.id}
                  isDownloading={downloadingId === file.conversion!.id}
                  isPending={false}
                />
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

export default History

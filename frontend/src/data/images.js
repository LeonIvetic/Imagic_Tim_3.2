import { useEffect, useState } from 'react'
import { useData } from './useData.js'

export const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/tiff', 'image/webp']
export const MAX_BYTES = 10 * 1024 * 1024

// Provjera prije slanja (NF-05). Backend svejedno provjerava sadržaj datoteke.
export function validateFile(file) {
  if (!ALLOWED_TYPES.includes(file.type)) {
    return `${file.name}: podržani su JPEG, PNG, TIFF i WebP.`
  }
  if (file.size > MAX_BYTES) return `${file.name}: slika je veća od 10 MB.`
  return null
}

// <img> ne može poslati Authorization zaglavlje, pa sliku dohvaćamo kao Blob
// i prikazujemo preko privremene blob: adrese (URL.createObjectURL).
// `stamp` (npr. updated_at) ponovno dohvaća sliku kad se promijeni.
export function useImageUrl(imageId, stamp) {
  const { getImageBlob } = useData()
  const [state, setState] = useState({ url: null, error: null })

  useEffect(() => {
    let url = null
    let cancelled = false
    setState({ url: null, error: null })
    getImageBlob(imageId)
      .then((blob) => {
        if (cancelled) return
        url = URL.createObjectURL(blob)
        setState({ url, error: null })
      })
      .catch((err) => !cancelled && setState({ url: null, error: err.message }))
    return () => {
      cancelled = true
      if (url) URL.revokeObjectURL(url)
    }
    // getImageBlob je stabilan za istu sesiju; ne ovisi o `version`.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [imageId, stamp])

  return state
}

// Preuzimanje izvorne datoteke pod imenom slike (F-002).
export async function downloadImage(data, image) {
  const blob = await data.getImageBlob(image.id, { original: true })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = image.name
  document.body.appendChild(a)
  a.click()
  a.remove()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}

export function formatBytes(bytes) {
  if (bytes == null) return '–'
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`
}

import { useMemo, useState } from 'react'
import { DataContext } from './useData.js'
import { useApiFetch } from '../api.js'

// Komponente pristupaju podacima samo kroz useData(), nikad izravno preko fetch-a.
// Funkcije odgovaraju REST rutama backenda (docs/4).

export function DataProvider({ children }) {
  const apiFetch = useApiFetch()
  // Povećava se nakon svake izmjene, pa se ekrani koji ovise o `version` ponovno učitaju.
  const [version, setVersion] = useState(0)

  const value = useMemo(() => {
    const json = (method, body) => ({ method, body: JSON.stringify(body) })

    // Omota funkciju koja mijenja podatke; nakon uspjeha osvježi prikaz.
    const mutation = (fn) => async (...args) => {
      const result = await fn(...args)
      setVersion((v) => v + 1)
      return result
    }

    return {
      version,

      // ---------- Korisnik ----------
      getMe: () => apiFetch('/api/users/me'),

      // ---------- Mape (F-003) ----------
      getRootFolder: () => apiFetch('/api/folders/root'),
      listAllFolders: () => apiFetch('/api/folders'),
      // → { folder, path, folders, images }
      listFolder: (folderId) => apiFetch(`/api/folders/${folderId}`),
      createFolder: mutation((parentId, name) =>
        apiFetch('/api/folders', json('POST', { parent_id: parentId, name })),
      ),
      renameFolder: mutation((id, name) => apiFetch(`/api/folders/${id}`, json('PATCH', { name }))),
      moveFolder: mutation((id, parentId) =>
        apiFetch(`/api/folders/${id}`, json('PATCH', { parent_id: parentId })),
      ),
      deleteFolder: mutation((id) => apiFetch(`/api/folders/${id}`, { method: 'DELETE' })),

      // ---------- Slike (F-002, F-004) ----------
      uploadImage: mutation((folderId, file) => {
        const form = new FormData()
        form.append('folder_id', folderId)
        form.append('file', file)
        return apiFetch('/api/images', { method: 'POST', body: form })
      }),
      // → ImageFile + { width, height, path }
      getImage: (id) => apiFetch(`/api/images/${id}`),
      // Blob za prikaz (TIFF dolazi pretvoren u PNG) ili izvorna datoteka.
      getImageBlob: (id, { original = false } = {}) =>
        apiFetch(`/api/images/${id}/${original ? 'file' : 'preview'}`, { as: 'blob' }),
      renameImage: mutation((id, name) => apiFetch(`/api/images/${id}`, json('PATCH', { name }))),
      moveImage: mutation((id, folderId) =>
        apiFetch(`/api/images/${id}`, json('PATCH', { folder_id: folderId })),
      ),
      deleteImage: mutation((id) => apiFetch(`/api/images/${id}`, { method: 'DELETE' })),
    }
  }, [apiFetch, version])

  return <DataContext.Provider value={value}>{children}</DataContext.Provider>
}

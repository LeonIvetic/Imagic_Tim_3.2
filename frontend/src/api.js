import { useCallback } from 'react'
import { useAuth0 } from '@auth0/auth0-react'

// Putanje počinju s /api — Vite proxy (vite.config.js) ih šalje na FastAPI (:8000).

// Hook koji vraća fetch funkciju koja automatski dodaje access token.
// Primjer:
//   const apiFetch = useApiFetch()
//   const me = await apiFetch('/api/users/me')
//   await apiFetch('/api/posts', { method: 'POST', body: JSON.stringify(data) })
export function useApiFetch() {
  const { getAccessTokenSilently } = useAuth0()

  return useCallback(
    async (path, options = {}) => {
      // Vraća token iz cachea ili tiho dohvaća novi kad stari istekne.
      const token = await getAccessTokenSilently()

      const headers = new Headers(options.headers)
      headers.set('Authorization', `Bearer ${token}`)
      if (options.body && !(options.body instanceof FormData)) {
        headers.set('Content-Type', 'application/json')
      }

      const response = await fetch(path, { ...options, headers })

      if (!response.ok) {
        const error = new Error(`API ${response.status}: ${path}`)
        error.status = response.status
        throw error
      }

      if (response.status === 204) return null
      return response.json()
    },
    [getAccessTokenSilently],
  )
}

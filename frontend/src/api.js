import { useCallback } from 'react'
import { useAuth0 } from '@auth0/auth0-react'

// Putanje počinju s /api — Vite proxy (vite.config.js) ih šalje na FastAPI (:8000).

const STATUS_MESSAGES = {
  401: 'Sesija je istekla. Prijavi se ponovno.',
  404: 'Traženi sadržaj ne postoji.',
  413: 'Datoteka je prevelika.',
  500: 'Greška na poslužitelju. Pokušaj ponovno.',
}

// Hook koji vraća fetch funkciju koja automatski dodaje access token.
// Primjer:
//   const apiFetch = useApiFetch()
//   const me = await apiFetch('/api/users/me')
//   await apiFetch('/api/folders', { method: 'POST', body: JSON.stringify(data) })
//   const blob = await apiFetch('/api/images/1/file', { as: 'blob' })
// Greška ima .message za korisnika (polje "detail" iz FastAPI-ja) i .status.
export function useApiFetch() {
  const { getAccessTokenSilently } = useAuth0()

  return useCallback(
    async (path, { as = 'json', ...options } = {}) => {
      // Vraća token iz cachea ili tiho dohvaća novi kad stari istekne.
      const token = await getAccessTokenSilently()

      const headers = new Headers(options.headers)
      headers.set('Authorization', `Bearer ${token}`)
      if (options.body && !(options.body instanceof FormData)) {
        headers.set('Content-Type', 'application/json')
      }

      let response
      try {
        response = await fetch(path, { ...options, headers })
      } catch {
        throw Object.assign(new Error('Poslužitelj nije dostupan.'), { status: 0 })
      }

      if (!response.ok) {
        let detail = null
        try {
          detail = (await response.json()).detail
        } catch {
          // tijelo nije JSON
        }
        // FastAPI za neispravan zahtjev (422) vraća popis grešaka, a ne tekst.
        if (Array.isArray(detail)) detail = detail.map((d) => d.msg).join(' ')
        const message = detail || STATUS_MESSAGES[response.status] || `Greška ${response.status}.`
        throw Object.assign(new Error(message), { status: response.status })
      }

      if (response.status === 204) return null
      if (as === 'blob') return response.blob()
      return response.json()
    },
    [getAccessTokenSilently],
  )
}

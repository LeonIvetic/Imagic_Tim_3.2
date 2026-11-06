import { useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react'
import { LoginButton, LogoutButton, SignupButton } from './auth/AuthButtons.jsx'
import RequireAuth from './auth/RequireAuth.jsx'
import { useApiFetch } from './api.js'
import './App.css'

// Privremena testna stranica za prijavu — zamijenit će je prave stranice.
function App() {
  const { isLoading, isAuthenticated, user } = useAuth0()

  return (
    <main style={{ padding: '2rem' }}>
      <header style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
        <h1>Imagic</h1>
        {!isLoading &&
          (isAuthenticated ? (
            <>
              <span>Bok, {user?.name ?? user?.email}</span>
              <LogoutButton />
            </>
          ) : (
            <>
              <LoginButton />
              <SignupButton />
            </>
          ))}
      </header>

      <RequireAuth>
        <MeTest />
      </RequireAuth>
    </main>
  )
}

// Poziva zaštićeni backend endpoint s tokenom.
function MeTest() {
  const apiFetch = useApiFetch()
  const [result, setResult] = useState(null)

  async function callMe() {
    try {
      setResult(await apiFetch('/api/me'))
    } catch (err) {
      setResult({ error: err.message })
    }
  }

  return (
    <section>
      <button type="button" onClick={callMe}>
        Pozovi GET /api/me
      </button>
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </section>
  )
}

export default App

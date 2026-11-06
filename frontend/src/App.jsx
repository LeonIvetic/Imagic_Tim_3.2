import { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react'
import { LoginButton, LogoutButton, SignupButton } from './auth/AuthButtons.jsx'
import { useApiFetch } from './api.js'
import './App.css'

function App() {
  const { isLoading, isAuthenticated, error } = useAuth0()

  // Kod neuspjele prijave SDK ostavi ?error=…&state=… u URL-u. Bez čišćenja bi
  // svako osvježavanje stranice ponovno obradilo stari state → "Invalid state".
  useEffect(() => {
    if (error && window.location.search.includes('state=')) {
      window.history.replaceState({}, document.title, window.location.pathname)
    }
  }, [error])

  if (isLoading) {
    return (
      <div className="splash">
        <Logo />
        <span className="spinner" aria-label="Učitavanje" />
      </div>
    )
  }

  return isAuthenticated ? <Home /> : <LoginPage error={error} />
}

function Logo({ light = false }) {
  return (
    <div className={`logo${light ? ' logo--light' : ''}`}>
      <span className="logo__mark" aria-hidden="true" />
      <span className="logo__text">Imagic</span>
    </div>
  )
}

/* ---------- Početna stranica za neprijavljene ---------- */

function LoginPage({ error }) {
  return (
    <div className="login">
      <aside className="login__brand">
        <Logo light />

        {/* Dekorativni prikaz "uređivanja slike", čisti CSS. */}
        <div className="showcase" aria-hidden="true">
          <div className="showcase__photo showcase__photo--back" />
          <div className="showcase__photo showcase__photo--mid" />
          <div className="showcase__photo showcase__photo--front">
            <span className="crop crop--tl" />
            <span className="crop crop--tr" />
            <span className="crop crop--bl" />
            <span className="crop crop--br" />
          </div>
          <div className="showcase__chip">
            <span className="showcase__label">Svjetlina</span>
            <span className="showcase__track">
              <span className="showcase__fill" />
            </span>
            <span className="showcase__value">+24</span>
          </div>
        </div>

        <p className="login__tagline">
          Obradi, spremi i podijeli svoje slike na jednom mjestu.
        </p>
      </aside>

      <main className="login__panel">
        <div className="login__card">
          <span className="eyebrow">Dobrodošli</span>
          <h1 className="login__title">
            Tvoje slike,
            <br />
            <em>tvoja pravila.</em>
          </h1>
          <p className="login__lead">
            Prijavi se kako bi pristupio svojoj radnoj okolini, mapama i objavama.
          </p>

          {error && (
            <div className="alert" role="alert">
              <strong>Prijava nije uspjela.</strong> {error.message}
            </div>
          )}

          <div className="login__actions">
            <LoginButton className="btn btn--primary btn--lg">Prijava</LoginButton>
            <SignupButton className="btn btn--secondary btn--lg">
              Izradi račun
            </SignupButton>
          </div>

          <p className="fineprint">
            <LockIcon />
            Prijava se odvija preko Auth0. Imagic nikad ne vidi ni ne pohranjuje tvoju
            lozinku.
          </p>
        </div>

        <footer className="login__footer">© 2026 Git Happens · FER</footer>
      </main>
    </div>
  )
}

function LockIcon() {
  return (
    <svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true">
      <path
        fill="currentColor"
        d="M12 2a5 5 0 0 0-5 5v3H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2h-1V7a5 5 0 0 0-5-5Zm-3 8V7a3 3 0 1 1 6 0v3H9Z"
      />
    </svg>
  )
}

/* ---------- Privremena stranica za prijavljene ---------- */

function Home() {
  const { user } = useAuth0()
  const name = user?.name ?? user?.email ?? 'korisniče'
  const firstName = name.split(' ')[0]

  return (
    <div className="shell">
      <header className="topbar">
        <Logo />
        <div className="topbar__user">
          <Avatar user={user} />
          <span className="topbar__name">{name}</span>
          <LogoutButton className="btn btn--ghost btn--sm" />
        </div>
      </header>

      <main className="shell__main">
        <section className="welcome">
          <span className="eyebrow">Prijavljen si</span>
          <h1>Bok, {firstName}.</h1>
          <p>Radna okolina stiže uskoro. Dotad možeš provjeriti vezu s backendom.</p>
        </section>

        <MeTest />
      </main>
    </div>
  )
}

function Avatar({ user }) {
  const [broken, setBroken] = useState(false)
  const initial = (user?.name ?? user?.email ?? '?').charAt(0).toUpperCase()

  if (user?.picture && !broken) {
    return (
      <img
        className="avatar"
        src={user.picture}
        alt=""
        referrerPolicy="no-referrer"
        onError={() => setBroken(true)}
      />
    )
  }
  return <span className="avatar avatar--initial">{initial}</span>
}

// Poziva zaštićeni backend endpoint s tokenom.
function MeTest() {
  const apiFetch = useApiFetch()
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  async function callMe() {
    setLoading(true)
    try {
      setResult({ ok: true, data: await apiFetch('/api/me') })
    } catch (err) {
      setResult({ ok: false, data: { error: err.message } })
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="card">
      <div className="card__head">
        <div>
          <h2>Test veze s backendom</h2>
          <p>
            Šalje <code>GET /api/me</code> s access tokenom.
          </p>
        </div>
        <button type="button" className="btn btn--primary" onClick={callMe} disabled={loading}>
          {loading ? 'Šaljem…' : 'Pošalji zahtjev'}
        </button>
      </div>

      {result && (
        <pre className={`result ${result.ok ? 'result--ok' : 'result--err'}`}>
          {JSON.stringify(result.data, null, 2)}
        </pre>
      )}
    </section>
  )
}

export default App

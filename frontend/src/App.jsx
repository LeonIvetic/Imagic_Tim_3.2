import { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react'
import { LoginButton, LogoutButton, SignupButton } from './auth/AuthButtons.jsx'
import { useApiFetch } from './api.js'
import './App.css'
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Logo from './components/Logo.jsx';
import Avatar from './components/Avatar.jsx';


import AppLayout from './layout/AppLayout.jsx';
import Workspace from './pages/Workspace.jsx';
import ImageViewer from './pages/ImageViewer.jsx';
import ArticGallery from './pages/ArticGallery.jsx';
import MyProfile from './pages/MyProfile.jsx';
import Users from './pages/Users.jsx';
import PublicProfile from './pages/PublicProfile.jsx';
import Favorites from './pages/Favorites.jsx';

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

  if (!isAuthenticated) {
    return (
      <LoginPage error={error} />
    )
  }

  return (

    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route index element={<Navigate to="/radna-okolina" replace />} />
          <Route path="radna-okolina/:folderId?" element={<Workspace />} />
          <Route path="slika/:imageId" element={<ImageViewer />} />
          <Route path="artic" element={<ArticGallery />} />
          <Route path="profil" element={<MyProfile />} />
          <Route path="korisnici" element={<Users />} />
          <Route path="korisnici/:username" element={<PublicProfile />} />
          <Route path="favoriti" element={<Favorites />} />
        </Route>
      </Routes>
    </BrowserRouter>
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


export default App

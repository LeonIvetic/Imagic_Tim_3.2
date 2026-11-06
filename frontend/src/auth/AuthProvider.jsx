import { Auth0Provider } from '@auth0/auth0-react'

// potrebni parametri 
const domain = import.meta.env.VITE_AUTH0_DOMAIN
const clientId = import.meta.env.VITE_AUTH0_CLIENT_ID
const audience = import.meta.env.VITE_AUTH0_AUDIENCE

if (!domain || !clientId || !audience) {
  throw new Error(
    'Auth0 varijable nisu postavljene. Kopiraj frontend/.env.example u frontend/.env i ponovno pokreni "npm run dev".',
  )
}

// Omata cijelu aplikaciju; nakon ovoga svaka komponenta može koristiti useAuth0().
export default function AuthProvider({ children }) {
  return (
    <Auth0Provider
      domain={domain}
      clientId={clientId}
      authorizationParams={{
        // Kamo Auth0 vraća korisnika nakon prijave (mora biti u "Allowed Callback URLs").
        redirect_uri: window.location.origin,
        // Bez audiencea Auth0 ne izdaje JWT koji backend može provjeriti.
        audience,
      }}
      // Refresh tokeni + localStorage: korisnik ostaje prijavljen nakon osvježavanja stranice.
      // U Auth0 aplikaciji treba uključiti "Refresh Token Rotation".
      useRefreshTokens
      cacheLocation="localstorage"
    >
      {children}
    </Auth0Provider>
  )
}

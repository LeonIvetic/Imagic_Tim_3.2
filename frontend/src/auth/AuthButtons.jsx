import { useAuth0 } from '@auth0/auth0-react'

// Svaki gumb prima opcionalni className i tekst (children), pa se može
// koristiti s različitim stilom na različitim mjestima.

export function LoginButton({ className = 'btn btn--primary', children = 'Prijava' }) {
  const { loginWithRedirect } = useAuth0()
  return (
    <button type="button" className={className} onClick={() => loginWithRedirect()}>
      {children}
    </button>
  )
}

export function SignupButton({ className = 'btn btn--secondary', children = 'Registracija' }) {
  const { loginWithRedirect } = useAuth0()
  return (
    <button
      type="button"
      className={className}
      onClick={() =>
        loginWithRedirect({ authorizationParams: { screen_hint: 'signup' } })
      }
    >
      {children}
    </button>
  )
}

export function LogoutButton({ className = 'btn btn--ghost', children = 'Odjava' }) {
  const { logout } = useAuth0()
  return (
    <button
      type="button"
      className={className}
      onClick={() =>
        // Mora biti u "Allowed Logout URLs" u Auth0.
        logout({ logoutParams: { returnTo: window.location.origin } })
      }
    >
      {children}
    </button>
  )
}

import { useAuth0 } from '@auth0/auth0-react'

export function LoginButton() {
  const { loginWithRedirect } = useAuth0()
  return (
    <button type="button" onClick={() => loginWithRedirect()}>
      Prijava
    </button>
  )
}

export function SignupButton() {
  const { loginWithRedirect } = useAuth0()
  return (
    <button
      type="button"
      onClick={() =>
        loginWithRedirect({ authorizationParams: { screen_hint: 'signup' } })
      }
    >
      Registracija
    </button>
  )
}

export function LogoutButton() {
  const { logout } = useAuth0()
  return (
    <button
      type="button"
      onClick={() =>
        // Mora biti u "Allowed Logout URLs" u Auth0.
        logout({ logoutParams: { returnTo: window.location.origin } })
      }
    >
      Odjava
    </button>
  )
}

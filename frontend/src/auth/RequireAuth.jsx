import { useAuth0 } from '@auth0/auth0-react'
import { LoginButton } from './AuthButtons.jsx'

// Omotaj sadržaj koji smije vidjeti samo prijavljeni korisnik:
//   <RequireAuth><Workspace /></RequireAuth>
// Ovo je samo UI zaštita — pravu zaštitu radi backend (401 bez valjanog tokena).
export default function RequireAuth({ children }) {
  const { isLoading, isAuthenticated } = useAuth0()

  if (isLoading) return <p>Učitavanje...</p>

  if (!isAuthenticated) {
    return (
      <div>
        <p>Za ovu stranicu moraš biti prijavljen.</p>
        <LoginButton />
      </div>
    )
  }

  return children
}

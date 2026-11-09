import {useState} from 'react';

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

export default Avatar
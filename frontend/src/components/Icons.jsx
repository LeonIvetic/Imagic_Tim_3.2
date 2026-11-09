function Icon({ children }) {
  return (
    <svg
      viewBox="0 0 24 24"
      width="22"
      height="22"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {children}
    </svg>
  )
}

export function FolderIcon() {
  return (
    <Icon>
      <path d="M3 6a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z" />
    </Icon>
  )
}

export function GalleryIcon() {
  return (
    <Icon>
      <rect x="3" y="4" width="18" height="16" rx="2" />
      <circle cx="15.5" cy="8.5" r="1.5" />
      <path d="m3 16 5-5 4 4 3-3 6 6" />
    </Icon>
  )
}

export function UserIcon() {
  return (
    <Icon>
      <circle cx="12" cy="8" r="4" />
      <path d="M4 21a8 8 0 0 1 16 0" />
    </Icon>
  )
}

export function UsersIcon() {
  return (
    <Icon>
      <circle cx="9" cy="8" r="3.5" />
      <path d="M2 20a7 7 0 0 1 14 0" />
      <circle cx="17" cy="9" r="2.5" />
      <path d="M18 14.5a5 5 0 0 1 4 5.5" />
    </Icon>
  )
}

export function StarIcon() {
  return (
    <Icon>
      <polygon points="12 3 14.8 8.9 21 9.6 16.4 13.9 17.6 20 12 16.9 6.4 20 7.6 13.9 3 9.6 9.2 8.9" />
    </Icon>
  )
}
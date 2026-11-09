
function Logo({ light = false }) {
  return (
    <div className={`logo${light ? ' logo--light' : ''}`}>
      <span className="logo__mark" aria-hidden="true" />
      <span className="logo__text">Imagic</span>
    </div>
  )
}

export default Logo
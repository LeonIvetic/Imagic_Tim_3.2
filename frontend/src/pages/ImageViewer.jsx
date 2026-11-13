import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useData } from '../data/useData.js'
import { downloadImage, formatBytes, useImageUrl } from '../data/images.js'
import Dialog, { NameDialog } from '../components/Dialog.jsx'
import './Workspace.css'

// Preglednik slike (F-004): slika, podaci o datoteci, preuzimanje.
export default function ImageViewer() {
  const { imageId } = useParams()
  const data = useData()
  const navigate = useNavigate()
  const [image, setImage] = useState(null)
  const [error, setError] = useState(null)
  const [fit, setFit] = useState(true)
  const [dialog, setDialog] = useState(null)

  useEffect(() => {
    let cancelled = false
    data
      .getImage(imageId)
      .then((img) => !cancelled && setImage(img))
      .catch((err) => !cancelled && setError(err.message))
    return () => {
      cancelled = true
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [imageId, data.version])

  if (error) {
    return (
      <div className="ws-state" role="alert">
        <p>{error}</p>
        <Link className="btn btn--secondary" to="/radna-okolina">
          Natrag na radnu okolinu
        </Link>
      </div>
    )
  }
  if (!image) return <div className="ws-state">Učitavanje…</div>

  const folder = image.path[image.path.length - 1]

  return (
    <div className="viewer">
      <header className="ws__head">
        <nav className="crumbs" aria-label="Putanja">
          {image.path.map((p) => (
            <span key={p.id} className="crumbs__item">
              <Link to={`/radna-okolina/${p.id}`}>{p.name}</Link>
            </span>
          ))}
          <span className="crumbs__item">
            <span aria-current="page">{image.name}</span>
          </span>
        </nav>
        <h1 className="ws__title viewer__title">{image.name}</h1>
      </header>

      <div className="viewer__layout">
        <figure className={`viewer__stage ${fit ? 'viewer__stage--fit' : ''}`}>
          <ViewerImage image={image} />
        </figure>

        <aside className="viewer__side">
          <div className="viewer__zoom" role="group" aria-label="Veličina prikaza">
            <button className={`btn btn--sm ${fit ? 'btn--primary' : 'btn--secondary'}`} onClick={() => setFit(true)}>
              Prilagodi
            </button>
            <button className={`btn btn--sm ${!fit ? 'btn--primary' : 'btn--secondary'}`} onClick={() => setFit(false)}>
              100 %
            </button>
          </div>

          <dl className="viewer__info">
            <dt>Format</dt>
            <dd>{image.format.toUpperCase()}</dd>
            <dt>Dimenzije</dt>
            <dd>{image.width ? `${image.width} × ${image.height} px` : '–'}</dd>
            <dt>Veličina</dt>
            <dd>{formatBytes(image.size_bytes)}</dd>
            <dt>Mapa</dt>
            <dd>
              <Link to={`/radna-okolina/${folder.id}`}>{folder.name}</Link>
            </dd>
            <dt>Učitano</dt>
            <dd>{new Date(image.created_at).toLocaleString('hr-HR')}</dd>
          </dl>

          <div className="viewer__actions">
            <button className="btn btn--primary" onClick={() => downloadImage(data, image)}>
              Preuzmi
            </button>
            <button className="btn btn--secondary" onClick={() => setDialog('rename')}>
              Preimenuj
            </button>
            <button className="btn btn--ghost btn--danger-text" onClick={() => setDialog('delete')}>
              Obriši
            </button>
          </div>

          <p className="viewer__note">Alati za obradu slike (filtri, morfologija, geometrija, segmentacija) dolaze u sljedećoj iteraciji.</p>
        </aside>
      </div>

      {dialog === 'rename' && (
        <NameDialog
          title="Preimenuj sliku"
          label="Novi naziv"
          initial={image.name}
          onSubmit={(name) => data.renameImage(image.id, name)}
          onClose={() => setDialog(null)}
        />
      )}
      {dialog === 'delete' && (
        <Dialog
          title="Obriši sliku?"
          submitLabel="Obriši"
          danger
          onSubmit={async () => {
            await data.deleteImage(image.id)
            navigate(`/radna-okolina/${folder.id}`, { replace: true })
          }}
          onClose={() => setDialog(null)}
        >
          <p>
            Slika <strong>{image.name}</strong> bit će trajno obrisana, kao i postovi u kojima se koristi.
          </p>
        </Dialog>
      )}
    </div>
  )
}

function ViewerImage({ image }) {
  const { url, error } = useImageUrl(image.id, image.updated_at)
  if (error) return <p role="alert">{error}</p>
  if (!url) return <span className="viewer__loading">Učitavanje slike…</span>
  return <img src={url} alt={image.name} />
}

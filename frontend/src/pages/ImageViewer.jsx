import { useEffect, useState, useRef } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useData } from '../data/useData.js'
import { downloadImage, formatBytes, splitImageName, useImageUrl } from '../data/images.js'
import Dialog, { NameDialog } from '../components/Dialog.jsx'
import './Workspace.css'

const FILTERS = {
  grayscale: 'Crno-bijelo',
  invert: 'Invertiranje',
  pixelate: 'Pikselizacija',
  blur: 'Zamućenje',
  derivative: 'Derivacija'
}

export default function ImageViewer() {
  const { imageId } = useParams()
  return <ImageViewerPage key={imageId} imageId={imageId} />
}

// Preglednik slike (F-004): slika, podaci o datoteci, preuzimanje.
function ImageViewerPage({ imageId }) {
  const data = useData()
  const navigate = useNavigate()
  const [image, setImage] = useState(null)
  const [error, setError] = useState(null)
  const [fit, setFit] = useState(true)
  const [dialog, setDialog] = useState(null)
  const [selectedFilter, setSelectedFilter] = useState('grayscale')
  const [draft, setDraft] = useState(null)
  const [filterBusy, setFilterBusy] = useState(false)
  const [filterError, setFilterError] = useState(null)

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

  async function previewFilter() {
    const request = {
      filters: [...(draft?.request.filters ?? []), selectedFilter],
      source_updated_at: draft?.request.source_updated_at ?? image.updated_at,
    }
    setFilterBusy(true)
    setFilterError(null)
    try {
      const blob = await data.previewFilters(image.id, request)
      // Blob svakog koraka čuvamo da poništavanje ne treba novi zahtjev.
      setDraft({ request, blobs: [...(draft?.blobs ?? []), blob] })
    } catch (err) {
      setFilterError(err.message)
    } finally {
      setFilterBusy(false)
    }
  }

  // Poništava zadnji filtar; nakon prvog se vraća prikaz izvorne slike.
  function undoFilter() {
    setFilterError(null)
    if (draft.request.filters.length === 1) {
      setDraft(null)
      return
    }
    setDraft({
      request: { ...draft.request, filters: draft.request.filters.slice(0, -1) },
      blobs: draft.blobs.slice(0, -1),
    })
  }

  async function saveFilterResult(action, name) {
    setFilterBusy(true)
    try {
      const saved = await data.saveFilters(image.id, { ...draft.request, action, name })
      setDraft(null)
      setFilterError(null)
      if (action === 'copy') navigate(`/slika/${saved.id}`)
    } finally {
      setFilterBusy(false)
    }
  }

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

  const { stem, suffix } = splitImageName(image.name, image.format)
  const copyStem = `${(stem || 'slika').slice(0, 240)}-obrada`

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
          {draft ? <DraftImage blob={draft.blobs[draft.blobs.length - 1]} name={image.name} /> : <ViewerImage image={image} />}
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

          <label className="field">
            <span className="field__label">Filtar</span>
            <select className="input" value={selectedFilter} onChange={(e) => setSelectedFilter(e.target.value)} disabled={filterBusy}>
              {Object.entries(FILTERS).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
            </select>
          </label>
          <div className="viewer__actions">
            <button className="btn btn--primary" onClick={previewFilter} disabled={filterBusy}>
              {filterBusy ? 'Obrada…' : 'Primijeni filtar'}
            </button>
            {draft && (
              <>
                <button className="btn btn--secondary" onClick={undoFilter} disabled={filterBusy}>
                  Poništi zadnji filtar
                </button>
                <button className="btn btn--secondary" onClick={() => setDialog('save-copy')} disabled={filterBusy}>
                  Spremi kao novu sliku
                </button>
                <button className="btn btn--secondary" onClick={() => setDialog('overwrite')} disabled={filterBusy}>
                  Prepiši izvornik
                </button>
                <button className="btn btn--ghost" disabled={filterBusy} onClick={() => {
                  setDraft(null)
                  setFilterError(null)
                }}>
                  Odbaci obradu
                </button>
              </>
            )}
          </div>
          {draft && (
            <p className="viewer__note">
              Primijenjeno: {draft.request.filters.map((name) => FILTERS[name]).join(' → ')}
            </p>
          )}
          {filterError && <p className="field-error" role="alert">{filterError}</p>}
        </aside>
      </div>

      {dialog === 'rename' && (
        <NameDialog
          title="Preimenuj sliku"
          label="Novi naziv"
          initial={stem}
          suffix={suffix}
          onSubmit={(name) => data.renameImage(image.id, name)}
          onClose={() => setDialog(null)}
        />
      )}
      {dialog === 'save-copy' && (
        <NameDialog
          title="Spremi kao novu sliku"
          label="Naziv nove datoteke"
          initial={copyStem}
          suffix={suffix}
          onSubmit={(name) => saveFilterResult('copy', name)}
          onClose={() => setDialog(null)}
        />
      )}
      {dialog === 'overwrite' && (
        <Dialog
          title="Prepisati izvornu sliku?"
          submitLabel="Prepiši izvornik"
          danger
          onSubmit={() => saveFilterResult('overwrite')}
          onClose={() => setDialog(null)}
        >
          <p>Obrađena slika zamijenit će izvornu i prikazivat će se u postojećim objavama koje je koriste.</p>
        </Dialog>
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

function DraftImage({ blob, name }) {
  const ref = useRef(null)
  useEffect(() => {
    const url = URL.createObjectURL(blob)
    ref.current.src = url
    return () => URL.revokeObjectURL(url)
  }, [blob])
  return <img ref={ref} alt={`Pregled obrade slike ${name}`} />
}
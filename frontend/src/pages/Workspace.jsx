import { useEffect, useRef, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { useData } from '../data/useData.js'
import { downloadImage, formatBytes, useImageUrl, validateFile } from '../data/images.js'
import Dialog, { NameDialog } from '../components/Dialog.jsx'
import { FolderIcon } from '../components/Icons.jsx'
import './Workspace.css'

// Radna okolina (UC-002): mape, upload, preimenovanje, premještanje, preuzimanje, brisanje.
export default function Workspace() {
  const data = useData()
  const { folderId } = useParams()
  const navigate = useNavigate()

  const [content, setContent] = useState(null) // { folder, path, folders, images }
  const [error, setError] = useState(null)
  const [dialog, setDialog] = useState(null) // { kind, item }
  const [notices, setNotices] = useState([]) // poruke nakon uploada
  const [uploading, setUploading] = useState(0)
  const [dragging, setDragging] = useState(false)
  const fileInput = useRef(null)

  // Bez :folderId u adresi otvara se korijenska mapa.
  useEffect(() => {
    let cancelled = false
    async function load() {
      try {
        const id = folderId ?? (await data.getRootFolder()).id
        const result = await data.listFolder(id)
        if (!cancelled) {
          setContent(result)
          setError(null)
        }
      } catch (err) {
        if (!cancelled) setError(err.message)
      }
    }
    load()
    return () => {
      cancelled = true
    }
    // data.version se mijenja nakon svake izmjene
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [folderId, data.version])

  async function uploadFiles(fileList) {
    const files = [...fileList]
    const messages = []
    const valid = files.filter((f) => {
      const problem = validateFile(f)
      if (problem) messages.push({ type: 'error', text: problem })
      return !problem
    })
    setUploading((n) => n + valid.length)
    for (const file of valid) {
      try {
        const image = await data.uploadImage(content.folder.id, file)
        messages.push({ type: 'ok', text: `Učitano: ${image.name}` })
      } catch (err) {
        messages.push({ type: 'error', text: `${file.name}: ${err.message}` })
      } finally {
        setUploading((n) => n - 1)
      }
    }
    setNotices(messages)
  }

  function onDrop(event) {
    event.preventDefault()
    setDragging(false)
    if (event.dataTransfer.files.length) uploadFiles(event.dataTransfer.files)
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
  if (!content) return <div className="ws-state">Učitavanje…</div>

  const { folder, path, folders, images } = content
  const isRoot = folder.parent_id === null
  const isEmpty = folders.length === 0 && images.length === 0

  return (
    <div
      className={`ws ${dragging ? 'ws--dragging' : ''}`}
      onDragOver={(e) => {
        e.preventDefault()
        setDragging(true)
      }}
      onDragLeave={(e) => e.currentTarget.contains(e.relatedTarget) || setDragging(false)}
      onDrop={onDrop}
    >
      <header className="ws__head">
        <nav className="crumbs" aria-label="Putanja">
          {path.map((p, i) => (
            <span key={p.id} className="crumbs__item">
              {i < path.length - 1 ? <Link to={`/radna-okolina/${p.id}`}>{p.name}</Link> : <span aria-current="page">{p.name}</span>}
            </span>
          ))}
        </nav>
        <div className="ws__title-row">
          <h1 className="ws__title">{folder.name}</h1>
          {!isRoot && (
            <div className="ws__folder-actions">
              <button className="btn btn--ghost btn--sm" onClick={() => setDialog({ kind: 'renameFolder', item: folder })}>
                Preimenuj
              </button>
              <button className="btn btn--ghost btn--sm" onClick={() => setDialog({ kind: 'moveFolder', item: folder })}>
                Premjesti
              </button>
              <button
                className="btn btn--ghost btn--sm btn--danger-text"
                onClick={() => setDialog({ kind: 'deleteFolder', item: folder })}
              >
                Obriši mapu
              </button>
            </div>
          )}
        </div>
        <div className="ws__toolbar">
          <button className="btn btn--primary" onClick={() => fileInput.current.click()}>
            Učitaj slike
          </button>
          <button className="btn btn--secondary" onClick={() => setDialog({ kind: 'createFolder' })}>
            Nova mapa
          </button>
          <input
            ref={fileInput}
            type="file"
            accept=".jpg,.jpeg,.png,.tif,.tiff,.webp,image/jpeg,image/png,image/tiff,image/webp"
            multiple
            hidden
            onChange={(e) => {
              uploadFiles(e.target.files)
              e.target.value = ''
            }}
          />
          <span className="ws__hint">ili povuci datoteke ovamo · JPEG, PNG, TIFF, WebP do 10 MB</span>
        </div>
      </header>

      {(uploading > 0 || notices.length > 0) && (
        <div className="notices" aria-live="polite">
          {uploading > 0 && <p className="notice">Učitavanje {uploading} slika…</p>}
          {notices.map((n, i) => (
            <p key={i} className={`notice notice--${n.type}`}>
              {n.text}
            </p>
          ))}
          {notices.length > 0 && uploading === 0 && (
            <button className="btn btn--ghost btn--sm" onClick={() => setNotices([])}>
              Zatvori
            </button>
          )}
        </div>
      )}

      {isEmpty ? (
        <div className="ws-empty">
          <FolderIcon />
          <p>Ova mapa je prazna.</p>
          <p className="ws-empty__sub">Povuci slike ovamo ili odaberi „Učitaj slike”.</p>
        </div>
      ) : (
        <ul className="grid" aria-label="Sadržaj mape">
          {folders.map((f) => (
            <li key={`f${f.id}`}>
              <button className="tile tile--folder" onClick={() => navigate(`/radna-okolina/${f.id}`)}>
                <FolderIcon />
                <span className="tile__name">{f.name}</span>
              </button>
            </li>
          ))}
          {images.map((img) => (
            <li key={`i${img.id}`}>
              <ImageTile image={img} onAction={(kind) => setDialog({ kind, item: img })} />
            </li>
          ))}
        </ul>
      )}

      {dialog && <WorkspaceDialog dialog={dialog} folder={folder} onClose={() => setDialog(null)} />}
    </div>
  )
}

function ImageTile({ image, onAction }) {
  const data = useData()
  const { url, error } = useImageUrl(image.id, image.updated_at)
  const [menu, setMenu] = useState(false)

  return (
    <div className="tile tile--image">
      <Link to={`/slika/${image.id}`} className="tile__thumb" aria-label={`Otvori ${image.name}`}>
        {url ? <img src={url} alt="" loading="lazy" /> : <span className="tile__ph">{error ? '!' : ''}</span>}
      </Link>
      <div className="tile__meta">
        <span className="tile__name" title={image.name}>
          {image.name}
        </span>
        <span className="tile__info">
          {image.format.toUpperCase()} · {formatBytes(image.size_bytes)}
        </span>
      </div>
      <div className="menu">
        <button
          className="menu__toggle"
          aria-label={`Radnje za ${image.name}`}
          aria-expanded={menu}
          onClick={() => setMenu((m) => !m)}
          onBlur={(e) => e.currentTarget.parentElement.contains(e.relatedTarget) || setMenu(false)}
        >
          ⋯
        </button>
        {menu && (
          <div className="menu__list" role="menu" onClick={() => setMenu(false)}>
            <button role="menuitem" onClick={() => onAction('renameImage')}>
              Preimenuj
            </button>
            <button role="menuitem" onClick={() => onAction('moveImage')}>
              Premjesti
            </button>
            <button role="menuitem" onClick={() => downloadImage(data, image)}>
              Preuzmi
            </button>
            <button role="menuitem" className="menu__danger" onClick={() => onAction('deleteImage')}>
              Obriši
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

function WorkspaceDialog({ dialog, folder, onClose }) {
  const data = useData()
  const navigate = useNavigate()
  const { kind, item } = dialog

  switch (kind) {
    case 'createFolder':
      return (
        <NameDialog
          title="Nova mapa"
          label="Naziv mape"
          submitLabel="Stvori"
          onSubmit={(name) => data.createFolder(folder.id, name)}
          onClose={onClose}
        />
      )
    case 'renameFolder':
    case 'renameImage':
      return (
        <NameDialog
          title={kind === 'renameFolder' ? 'Preimenuj mapu' : 'Preimenuj sliku'}
          label="Novi naziv"
          initial={item.name}
          onSubmit={(name) => (kind === 'renameFolder' ? data.renameFolder(item.id, name) : data.renameImage(item.id, name))}
          onClose={onClose}
        />
      )
    case 'moveFolder':
    case 'moveImage':
      return <MoveDialog kind={kind} item={item} onClose={onClose} />
    case 'deleteFolder':
      return (
        <Dialog
          title="Obriši mapu?"
          submitLabel="Obriši"
          danger
          onSubmit={async () => {
            await data.deleteFolder(item.id)
            // replace: povratak u pregledniku ne vodi na obrisanu mapu
            navigate(`/radna-okolina/${item.parent_id}`, { replace: true })
          }}
          onClose={onClose}
        >
          <p>
            Mapa <strong>{item.name}</strong> bit će obrisana zajedno sa svim podmapama i slikama u njoj. Ovo se ne može
            poništiti.
          </p>
        </Dialog>
      )
    case 'deleteImage':
      return (
        <Dialog title="Obriši sliku?" submitLabel="Obriši" danger onSubmit={() => data.deleteImage(item.id)} onClose={onClose}>
          <p>
            Slika <strong>{item.name}</strong> bit će trajno obrisana, kao i postovi u kojima se koristi.
          </p>
        </Dialog>
      )
    default:
      return null
  }
}

// Odabir odredišne mape iz stabla svih korisnikovih mapa.
function MoveDialog({ kind, item, onClose }) {
  const data = useData()
  const [options, setOptions] = useState(null)
  const [target, setTarget] = useState('')
  const isFolder = kind === 'moveFolder'
  const current = isFolder ? item.parent_id : item.folder_id

  useEffect(() => {
    data.listAllFolders().then((all) => {
      const children = new Map()
      for (const f of all) {
        if (!children.has(f.parent_id)) children.set(f.parent_id, [])
        children.get(f.parent_id).push(f)
      }
      const list = []
      // Mapa se ne smije premjestiti u samu sebe ni u svoju podmapu.
      const walk = (parentId, depth) => {
        for (const f of children.get(parentId) ?? []) {
          if (isFolder && f.id === item.id) continue
          list.push({ ...f, depth })
          walk(f.id, depth + 1)
        }
      }
      walk(null, 0)
      setOptions(list)
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <Dialog
      title={`Premjesti ${isFolder ? 'mapu' : 'sliku'}`}
      submitLabel="Premjesti"
      onSubmit={() => {
        const id = Number(target)
        return isFolder ? data.moveFolder(item.id, id) : data.moveImage(item.id, id)
      }}
      onClose={onClose}
    >
      <p>
        Odaberi kamo premjestiti <strong>{item.name}</strong>.
      </p>
      <label className="field">
        <span className="field__label">Odredišna mapa</span>
        <select className="input" required value={target} onChange={(e) => setTarget(e.target.value)} disabled={!options}>
          <option value="" disabled>
            {options ? 'Odaberi mapu' : 'Učitavanje…'}
          </option>
          {options?.map((f) => (
            <option key={f.id} value={f.id} disabled={f.id === current}>
              {'  '.repeat(f.depth)}
              {f.name}
              {f.id === current ? ' (trenutačna)' : ''}
            </option>
          ))}
        </select>
      </label>
    </Dialog>
  )
}

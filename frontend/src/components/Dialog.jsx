import { useEffect, useRef, useState } from 'react'

// Modalni dijalog (nativni <dialog>): Esc i klik izvan zatvaraju ga.
// onSubmit može baciti grešku; poruka se prikazuje u dijalogu, a dijalog ostaje otvoren.
export default function Dialog({ title, children, submitLabel = 'Spremi', danger = false, onSubmit, onClose }) {
  const ref = useRef(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    const dialog = ref.current
    dialog.showModal()
    return () => dialog.close()
  }, [])

  async function handleSubmit(event) {
    event.preventDefault()
    setBusy(true)
    setError(null)
    try {
      await onSubmit()
      onClose()
    } catch (err) {
      setError(err.message)
      setBusy(false)
    }
  }

  return (
    <dialog
      ref={ref}
      className="dialog"
      onCancel={(e) => {
        e.preventDefault()
        onClose()
      }}
      onClick={(e) => e.target === ref.current && onClose()}
    >
      <form className="dialog__body" onSubmit={handleSubmit}>
        <h2 className="dialog__title">{title}</h2>
        {children}
        {error && (
          <p className="field-error" role="alert">
            {error}
          </p>
        )}
        <div className="dialog__actions">
          <button type="button" className="btn btn--ghost" onClick={onClose}>
            Odustani
          </button>
          <button type="submit" className={`btn ${danger ? 'btn--danger' : 'btn--primary'}`} disabled={busy}>
            {busy ? 'Spremanje…' : submitLabel}
          </button>
        </div>
      </form>
    </dialog>
  )
}

// Dijalog s jednim tekstualnim poljem (nova mapa, preimenovanje).
export function NameDialog({ title, label, initial = '', submitLabel, onSubmit, onClose }) {
  const [name, setName] = useState(initial)
  const inputRef = useRef(null)

  useEffect(() => {
    const input = inputRef.current
    input.focus()
    // Kod preimenovanja slike označi ime bez nastavka.
    const dot = initial.lastIndexOf('.')
    input.setSelectionRange(0, dot > 0 ? dot : initial.length)
  }, [initial])

  return (
    <Dialog title={title} submitLabel={submitLabel} onSubmit={() => onSubmit(name)} onClose={onClose}>
      <label className="field">
        <span className="field__label">{label}</span>
        <input
          ref={inputRef}
          className="input"
          value={name}
          maxLength={255}
          required
          onChange={(e) => setName(e.target.value)}
        />
      </label>
    </Dialog>
  )
}

// Privremeni ekran za funkcionalnosti planirane u sljedećim iteracijama.
export default function ComingSoon({ title, text }) {
  return (
    <div className="ws-state ws-state--soon">
      <span className="eyebrow">U izradi</span>
      <h1 className="ws__title">{title}</h1>
      <p>{text}</p>
    </div>
  )
}

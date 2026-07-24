/**
 * Scritta colorata usata al posto del logo grafico negli header dell'app
 * (onboarding, schermata codice, shell principale): un solo posto per
 * cambiare nome/colori del brand invece di ripetere il markup ovunque.
 */
export default function BrandWordmark({ className = "" }) {
  return (
    <div className={`font-extrabold tracking-tight leading-none ${className}`}>
      <span className="text-office">Smart Working</span> <span className="text-ink">Manager</span>
    </div>
  );
}

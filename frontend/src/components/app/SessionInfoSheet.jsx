import { useState } from "react";
import { useSession } from "../../context/SessionContext.jsx";

export default function SessionInfoSheet({ onClose }) {
  const { session, deleteSession } = useSession();
  const [confirming, setConfirming] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [copied, setCopied] = useState(false);

  const code = session?.code || "";

  const copyCode = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Clipboard non disponibile: l'utente può selezionare il codice a mano.
    }
  };

  const handleDelete = async () => {
    setDeleting(true);
    try {
      await deleteSession();
      // Dopo l'eliminazione lo stato torna a 'onboarding': lo sheet non serve più.
    } catch {
      setDeleting(false);
    }
  };

  return (
    <>
      <div onClick={onClose} className="absolute inset-0 bg-black/40 z-10 animate-wl-fade" />
      <div
        className="absolute left-0 right-0 bottom-0 bg-surface rounded-t-[22px] px-5 z-20 animate-wl-sheet-up"
        style={{ paddingTop: 18, paddingBottom: "calc(22px + env(safe-area-inset-bottom, 0px))" }}
      >
        <div className="w-9 h-1 rounded-full bg-line mx-auto mb-4" />

        <div className="bg-ink rounded-[18px] p-[22px] mb-3.5 text-white">
          <div className="text-xs font-bold opacity-65 uppercase tracking-wide mb-1.5">
            Il tuo codice personale
          </div>
          <div className="text-2xl font-extrabold tracking-tight leading-none font-mono">{code}</div>
        </div>

        <button
          onClick={copyCode}
          type="button"
          className="w-full px-4 py-3.5 rounded-2xl border-[1.5px] border-line bg-surface font-extrabold text-[15px] text-ink mb-2.5"
        >
          {copied ? "Copiato ✓" : "Copia codice"}
        </button>

        {!confirming ? (
          <button
            onClick={() => setConfirming(true)}
            type="button"
            className="w-full py-3 border-none bg-transparent text-pace-red text-[13px] font-bold"
          >
            Elimina sessione e i tuoi dati
          </button>
        ) : (
          <div className="flex flex-col gap-2.5 px-4 py-3.5 rounded-2xl bg-pace-red-soft">
            <div className="text-[13px] font-bold text-pace-red">
              Eliminare definitivamente la sessione e tutti i tuoi dati?
            </div>
            <div className="text-xs text-muted leading-relaxed">
              Presenze registrate, azienda e codice andranno persi per sempre. Non si può
              annullare.
            </div>
            <div className="flex gap-2 mt-1">
              <button
                type="button"
                onClick={() => setConfirming(false)}
                disabled={deleting}
                className="shrink-0 px-3.5 py-2.5 rounded-xl border-[1.5px] border-line bg-surface font-bold text-xs text-ink disabled:opacity-50"
              >
                Annulla
              </button>
              <button
                type="button"
                onClick={handleDelete}
                disabled={deleting}
                className="flex-1 py-2.5 rounded-xl border-none font-bold text-xs text-white bg-pace-red disabled:opacity-60"
              >
                {deleting ? "Eliminazione…" : "Sì, elimina tutto"}
              </button>
            </div>
          </div>
        )}
      </div>
    </>
  );
}

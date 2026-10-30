import { useEffect } from "react";

const STEPS = [
  {
    title: "Parti senza registrazione",
    text: "Niente account né password: scegli un nickname (max 10 caratteri), cerca la tua azienda, imposta la policy e inizia. Alla fine ricevi un codice personale (SW-XXXX-XXXX): conservalo, serve per ritrovare i tuoi dati da un altro dispositivo o se il browser dimentica la sessione.",
  },
  {
    title: "Imposti la policy",
    text: "Percentuale di presenza in ufficio (es. 60%) oppure giorni fissi a settimana (es. 3). Scegli da quando iniziare a monitorare e, se serve, entro quando raggiungere l'obiettivo: i giorni richiesti si calcolano solo in quel periodo.",
  },
  {
    title: "Registri le giornate",
    text: "Dalla Dashboard segni la giornata di oggi con un tocco; dal Calendario puoi aggiungere o correggere qualsiasi giorno. Tipologie: Ufficio, Smart working, Ferie, Permesso, Malattia, Trasferta.",
  },
  {
    title: "Cosa conta nel calcolo",
    text: "Ufficio e Trasferta contano come giorni in ufficio. Lo Smart working conta come giorno fuori sede. Ferie, Permessi e Malattia sono registrati ma non pesano né sull'ufficio né sullo smart working. I giorni prima della data di inizio non vengono contati.",
  },
  {
    title: "Leggi l'andamento",
    text: "L'anello mostra i giorni in ufficio fatti rispetto a quelli richiesti. Il semaforo verde, arancio o rosso confronta il tuo ritmo con quello atteso fino a oggi. Trovi anche la scadenza, i giorni rimanenti e la percentuale di giorni registrati fino a oggi.",
  },
  {
    title: "Simuli gli scenari",
    text: "Nella scheda Simulazione ipotizzi giorni futuri in ufficio o in smart working e vedi subito l'effetto sull'obiettivo, senza salvare nulla.",
  },
  {
    title: "Modifichi quando vuoi",
    text: "Con l'icona a ingranaggio cambi policy, data di inizio e scadenza. Toccando il tuo nickname rivedi il codice e, se vuoi, elimini definitivamente sessione e dati.",
  },
];

export default function HowItWorksModal({ onClose }) {
  useEffect(() => {
    const onKey = (e) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  return (
    <div className="absolute inset-0 z-30 flex items-end sm:items-center justify-center">
      <div onClick={onClose} className="absolute inset-0 bg-black/40 animate-wl-fade" />
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="how-it-works-title"
        className="relative w-full max-h-[88%] bg-surface rounded-t-[22px] sm:rounded-[22px] sm:mx-3
                   flex flex-col animate-wl-sheet-up"
      >
        <div className="shrink-0 flex items-center justify-between px-5 pt-[18px] pb-3 border-b border-line">
          <h2 id="how-it-works-title" className="text-lg font-extrabold tracking-tight">
            Come funziona
          </h2>
          <button
            type="button"
            onClick={onClose}
            aria-label="Chiudi"
            className="w-8 h-8 rounded-[10px] border-[1.5px] border-line bg-white text-ink font-bold leading-none"
          >
            ×
          </button>
        </div>

        <div className="overflow-y-auto px-5 py-4">
          <p className="text-[13px] text-muted leading-relaxed mb-4">
            Smart Working Manager ti aiuta a rispettare la policy di presenza in ufficio della tua
            azienda: registri le giornate, vedi a che punto sei e se sei in linea con l'obiettivo.
          </p>
          <ol className="flex flex-col gap-3.5 mb-2">
            {STEPS.map((s, i) => (
              <li key={s.title} className="flex gap-3">
                <div className="shrink-0 w-6 h-6 rounded-full bg-office-soft text-office text-xs font-extrabold flex items-center justify-center">
                  {i + 1}
                </div>
                <div>
                  <div className="text-[13.5px] font-extrabold mb-0.5">{s.title}</div>
                  <div className="text-[12.5px] text-muted leading-relaxed">{s.text}</div>
                </div>
              </li>
            ))}
          </ol>
        </div>

        <div
          className="shrink-0 px-5 pt-2"
          style={{ paddingBottom: "calc(16px + env(safe-area-inset-bottom, 0px))" }}
        >
          <button
            type="button"
            onClick={onClose}
            className="w-full p-3.5 rounded-2xl border-none font-extrabold text-[14px] text-white bg-ink"
          >
            Ho capito
          </button>
        </div>
      </div>
    </div>
  );
}

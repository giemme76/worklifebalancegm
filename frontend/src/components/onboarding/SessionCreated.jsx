import { useState } from "react";
import { useSession } from "../../context/SessionContext.jsx";
import BrandWordmark from "../BrandWordmark.jsx";

export default function SessionCreated() {
  const { session, enterApp } = useSession();
  const [copied, setCopied] = useState(false);

  const code = session?.code || "";
  const nickname = session?.nickname;

  const copyCode = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Clipboard non disponibile (es. contesto non sicuro): l'utente può
      // comunque selezionare e copiare il codice a mano.
    }
  };

  return (
    <div className="flex flex-col h-full px-[22px] py-6 overflow-y-auto">
      <div className="flex items-center mb-7">
        <BrandWordmark className="text-2xl" />
      </div>

      <div className="flex items-center gap-2.5 mb-2">
        <div className="w-2.5 h-2.5 rounded-full bg-office shrink-0" />
        <div className="text-2xl font-extrabold tracking-tight leading-tight">
          Sessione creata{nickname ? `, ${nickname}!` : "!"}
        </div>
      </div>
      <div className="text-sm text-muted leading-relaxed mb-6">
        Conserva questo codice: è l'unico modo per recuperare i tuoi dati se cambi
        dispositivo o il browser dimentica l'accesso.
      </div>

      <div className="bg-ink rounded-[18px] p-[22px] mb-3.5 text-white">
        <div className="text-xs font-bold opacity-65 uppercase tracking-wide mb-1.5">
          Il tuo codice personale
        </div>
        <div className="text-2xl font-extrabold tracking-tight leading-none font-mono">
          {code}
        </div>
      </div>

      <button
        onClick={copyCode}
        type="button"
        className="px-4 py-3.5 rounded-2xl border-[1.5px] border-line bg-surface font-extrabold text-[15px] text-ink mb-3.5"
      >
        {copied ? "Copiato ✓" : "Copia codice"}
      </button>

      <div className="flex-1" />

      <button
        onClick={enterApp}
        type="button"
        className="p-4 rounded-2xl font-extrabold text-[15px] text-white bg-ink cursor-pointer"
      >
        Vai alla Dashboard
      </button>
    </div>
  );
}

import { useEffect, useRef, useState } from "react";
import { api } from "../../api/client.js";

const SEARCH_DEBOUNCE_MS = 400;

export default function StepCompany({
  nickname,
  setNickname,
  companyName,
  setCompanyName,
  detected,
  setDetected,
  city,
  setCity,
  onNext,
}) {
  const [results, setResults] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [searching, setSearching] = useState(false);
  const [searchFailed, setSearchFailed] = useState(false);
  const debounceRef = useRef(null);
  const requestIdRef = useRef(0);

  const runSearch = (value) => {
    const requestId = ++requestIdRef.current;
    setSearching(true);
    setSearchFailed(false);
    api
      .searchCompany(value)
      .then((data) => {
        if (requestId !== requestIdRef.current) return; // risposta di una ricerca superata
        const found = data?.results || [];
        setResults(found);
        setSelectedIndex(0);
        setDetected(found.length > 0);
        setCity(found[0]?.city || "");
      })
      .catch(() => {
        if (requestId !== requestIdRef.current) return;
        setResults([]);
        setDetected(false);
        setCity("");
        setSearchFailed(true);
      })
      .finally(() => {
        if (requestId === requestIdRef.current) setSearching(false);
      });
  };

  const onChange = (e) => {
    const value = e.target.value;
    setCompanyName(value);

    if (debounceRef.current) clearTimeout(debounceRef.current);

    const trimmed = value.trim();
    if (trimmed.length <= 2) {
      requestIdRef.current += 1; // invalida eventuali ricerche in corso
      setResults([]);
      setDetected(false);
      setSearching(false);
      setSearchFailed(false);
      setCity("");
      return;
    }

    debounceRef.current = setTimeout(() => runSearch(trimmed), SEARCH_DEBOUNCE_MS);
  };

  useEffect(() => () => clearTimeout(debounceRef.current), []);

  const cycleCity = () => {
    if (results.length === 0) return;
    const next = (selectedIndex + 1) % results.length;
    setSelectedIndex(next);
    setCity(results[next].city || "");
  };

  const manualCityEntry = companyName.trim().length > 2 && !searching && results.length === 0;
  const disabled = !(companyName.trim() && (detected ? city : city.trim()));

  return (
    <div className="flex flex-col flex-1">
      <div className="flex flex-col gap-1.5 px-4 py-3.5 rounded-2xl bg-office-soft mb-6">
        <div className="text-[13px] font-bold text-ink">Cos'è WorkLifeBalanceGM</div>
        <div className="text-xs text-muted leading-relaxed">
          Ti aiuta a tenere traccia delle giornate in ufficio e in smart working, a capire
          a colpo d'occhio se sei in linea con la policy aziendale e a organizzare le
          settimane in anticipo.
        </div>
      </div>

      <div className="text-2xl font-extrabold tracking-tight leading-tight mb-2">
        Come ti chiami?
      </div>
      <div className="text-sm text-muted leading-relaxed mb-3.5">
        Useremo il tuo nome per personalizzare l'app (facoltativo).
      </div>

      <input
        type="text"
        placeholder="Es. Guido"
        value={nickname}
        onChange={(e) => setNickname(e.target.value)}
        className="w-full px-4 py-3.5 rounded-2xl border-[1.5px] border-line text-base font-semibold
                   text-ink bg-surface outline-none mb-6 focus:border-ink transition-colors"
      />

      <div className="text-2xl font-extrabold tracking-tight leading-tight mb-2">
        Qual è la tua azienda?
      </div>
      <div className="text-sm text-muted leading-relaxed mb-6">
        Useremo il nome per rilevare la sede e la policy di smart working.
      </div>

      <input
        type="text"
        placeholder="Es. Aurora Systems S.p.A."
        value={companyName}
        onChange={onChange}
        className="w-full px-4 py-3.5 rounded-2xl border-[1.5px] border-line text-base font-semibold
                   text-ink bg-surface outline-none mb-3.5 focus:border-ink transition-colors"
      />

      {searching && <div className="text-xs text-muted mb-3.5 px-1">Ricerca in corso…</div>}

      {detected && results.length > 0 && (
        <div className="flex items-center gap-2.5 px-4 py-3.5 rounded-2xl bg-office-soft mb-3.5 animate-wl-fade">
          <div className="w-2.5 h-2.5 rounded-full bg-office shrink-0" />
          <div className="flex-1">
            <div className="text-[13px] font-bold">Sede rilevata: {city || "—"}</div>
            <div className="text-xs text-muted">
              {results[selectedIndex]?.name}
              {results[selectedIndex]?.address ? ` — ${results[selectedIndex].address}` : ""}
            </div>
          </div>
          {results.length > 1 && (
            <button
              onClick={cycleCity}
              className="border-none bg-transparent text-xs font-bold text-office cursor-pointer px-1"
              type="button"
            >
              Cambia
            </button>
          )}
        </div>
      )}

      {manualCityEntry && (
        <div className="flex flex-col gap-1.5 px-4 py-3.5 rounded-2xl bg-surface border-[1.5px] border-line mb-3.5">
          <div className="text-[13px] font-bold">
            {searchFailed ? "Ricerca non disponibile" : "Nessuna sede trovata automaticamente"}
          </div>
          <div className="text-xs text-muted mb-1.5">Inserisci la città della sede principale</div>
          <input
            type="text"
            placeholder="Es. Milano"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            className="w-full px-3.5 py-2.5 rounded-xl border-[1.5px] border-line text-sm font-semibold
                       text-ink bg-white outline-none focus:border-ink transition-colors"
          />
        </div>
      )}

      <div className="flex-1" />

      <button
        onClick={onNext}
        disabled={disabled}
        type="button"
        className={`p-4 rounded-2xl font-extrabold text-[15px] text-white bg-ink
                    ${disabled ? "opacity-40 pointer-events-none" : "cursor-pointer"}`}
      >
        Continua
      </button>
    </div>
  );
}

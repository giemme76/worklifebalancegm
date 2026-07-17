import { CITIES } from "../../lib/cities.js";

export default function StepCompany({
  companyName,
  setCompanyName,
  detected,
  setDetected,
  city,
  setCity,
  onNext,
}) {
  const onChange = (e) => {
    const value = e.target.value;
    setCompanyName(value);
    const isDetected = value.trim().length > 2;
    setDetected(isDetected);
    if (isDetected && !city) {
      setCity(CITIES[value.trim().length % CITIES.length]);
    }
    if (!isDetected) setCity("");
  };

  const cycleCity = () => {
    setCity(CITIES[(CITIES.indexOf(city) + 1) % CITIES.length]);
  };

  const disabled = !(companyName.trim() && detected);

  return (
    <div className="flex flex-col flex-1">
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

      {detected && (
        <div className="flex items-center gap-2.5 px-4 py-3.5 rounded-2xl bg-office-soft mb-3.5 animate-wl-fade">
          <div className="w-2.5 h-2.5 rounded-full bg-office shrink-0" />
          <div className="flex-1">
            <div className="text-[13px] font-bold">Sede rilevata: {city}</div>
            <div className="text-xs text-muted">
              Sede aziendale principale, individuata automaticamente
            </div>
          </div>
          <button
            onClick={cycleCity}
            className="border-none bg-transparent text-xs font-bold text-office cursor-pointer px-1"
            type="button"
          >
            Cambia
          </button>
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

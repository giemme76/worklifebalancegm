export default function StepPolicy({
  companyName,
  policyType,
  setPolicyType,
  policyPercent,
  setPolicyPercent,
  policyDays,
  setPolicyDays,
  onBack,
  onNext,
}) {
  const isPercent = policyType === "PERCENT";

  return (
    <div className="flex flex-col flex-1">
      <div className="text-2xl font-extrabold tracking-tight leading-tight mb-2">
        Qual è la policy?
      </div>
      <div className="text-sm text-muted leading-relaxed mb-5">
        Come {companyName || "la tua azienda"} definisce la presenza in ufficio.
      </div>

      <div className="flex bg-surface border-[1.5px] border-line rounded-2xl p-1 mb-5">
        <button
          type="button"
          onClick={() => setPolicyType("PERCENT")}
          className={`flex-1 py-2.5 rounded-xl text-[13px] font-bold transition-colors ${
            isPercent ? "bg-ink text-white" : "text-muted"
          }`}
        >
          Percentuale
        </button>
        <button
          type="button"
          onClick={() => setPolicyType("FIXED_DAYS")}
          className={`flex-1 py-2.5 rounded-xl text-[13px] font-bold transition-colors ${
            !isPercent ? "bg-ink text-white" : "text-muted"
          }`}
        >
          Giorni fissi
        </button>
      </div>

      {isPercent ? (
        <div className="bg-surface border-[1.5px] border-line rounded-2xl p-5 mb-4">
          <div className="text-[13px] text-muted font-semibold mb-1.5">
            Giorni in ufficio richiesti
          </div>
          <div className="text-[38px] font-extrabold tracking-tight mb-3.5">
            {policyPercent}%
          </div>
          <input
            type="range"
            min={0}
            max={100}
            step={5}
            value={policyPercent}
            onChange={(e) => setPolicyPercent(Number(e.target.value))}
            className="w-full accent-office"
          />
          <div className="flex justify-between text-[11px] text-muted mt-1">
            <span>0%</span>
            <span>100%</span>
          </div>
          <div className="text-xs text-muted mt-3">
            Corrisponde a <span className="font-bold text-ink">{100 - policyPercent}%</span> di
            smart working
          </div>
        </div>
      ) : (
        <div className="bg-surface border-[1.5px] border-line rounded-2xl p-5 mb-4">
          <div className="text-[13px] text-muted font-semibold mb-3.5">
            Giorni ufficio a settimana
          </div>
          <div className="flex items-center justify-center gap-5">
            <button
              type="button"
              onClick={() => setPolicyDays(Math.max(1, policyDays - 1))}
              className="w-11 h-11 rounded-xl border-[1.5px] border-line bg-surface text-xl font-bold text-ink"
            >
              –
            </button>
            <div className="text-[38px] font-extrabold min-w-[56px] text-center tracking-tight">
              {policyDays}
            </div>
            <button
              type="button"
              onClick={() => setPolicyDays(Math.min(5, policyDays + 1))}
              className="w-11 h-11 rounded-xl border-[1.5px] border-line bg-surface text-xl font-bold text-ink"
            >
              +
            </button>
          </div>
        </div>
      )}

      <div className="flex-1" />

      <div className="flex gap-2.5">
        <button
          type="button"
          onClick={onBack}
          className="shrink-0 px-[18px] py-4 rounded-2xl border-[1.5px] border-line bg-surface font-extrabold text-[15px] text-ink"
        >
          Indietro
        </button>
        <button
          type="button"
          onClick={onNext}
          className="flex-1 p-4 rounded-2xl border-none font-extrabold text-[15px] text-white bg-ink"
        >
          Continua
        </button>
      </div>
    </div>
  );
}

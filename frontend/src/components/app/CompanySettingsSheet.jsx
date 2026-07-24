import { useState } from "react";
import { useSession } from "../../context/SessionContext.jsx";

export default function CompanySettingsSheet({ onClose }) {
  const { session, updateCompanySettings } = useSession();
  const company = session?.company;

  const [policyType, setPolicyType] = useState(company?.policy_type || "PERCENT");
  const [policyPercent, setPolicyPercent] = useState(
    company?.policy_type === "PERCENT" && company?.smart_working_percentage != null
      ? 100 - company.smart_working_percentage
      : 60
  );
  const [policyDays, setPolicyDays] = useState(company?.office_days_per_week || 3);
  const [monitoringStartDate, setMonitoringStartDate] = useState(
    company?.monitoring_start_date || new Date().toISOString().slice(0, 10)
  );

  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  const isPercent = policyType === "PERCENT";

  const handleSave = async () => {
    setSaving(true);
    setError(null);
    try {
      await updateCompanySettings({
        policy_type: policyType,
        smart_working_percentage: isPercent ? 100 - policyPercent : undefined,
        office_days_per_week: !isPercent ? policyDays : undefined,
        work_days_per_week: company?.work_days_per_week || 5,
        monitoring_start_date: monitoringStartDate,
      });
      onClose();
    } catch {
      setError("Non è stato possibile salvare le impostazioni. Riprova.");
      setSaving(false);
    }
  };

  return (
    <>
      <div onClick={onClose} className="absolute inset-0 bg-black/40 z-10 animate-wl-fade" />
      <div
        className="absolute left-0 right-0 bottom-0 bg-surface rounded-t-[22px] px-5 z-20 animate-wl-sheet-up
                   max-h-[88%] overflow-y-auto"
        style={{ paddingTop: 18, paddingBottom: "calc(22px + env(safe-area-inset-bottom, 0px))" }}
      >
        <div className="w-9 h-1 rounded-full bg-line mx-auto mb-4" />

        <div className="text-lg font-extrabold tracking-tight mb-1">Impostazioni</div>
        <div className="text-xs text-muted mb-4">Policy aziendale e data di inizio monitoraggio.</div>

        <div className="flex bg-white border-[1.5px] border-line rounded-2xl p-1 mb-4">
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
          <div className="bg-white border-[1.5px] border-line rounded-2xl p-5 mb-4">
            <div className="text-[13px] text-muted font-semibold mb-1.5">
              Giorni in ufficio richiesti
            </div>
            <div className="text-[32px] font-extrabold tracking-tight mb-3">{policyPercent}%</div>
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
          </div>
        ) : (
          <div className="bg-white border-[1.5px] border-line rounded-2xl p-5 mb-4">
            <div className="text-[13px] text-muted font-semibold mb-3">
              Giorni ufficio a settimana
            </div>
            <div className="flex items-center justify-center gap-5">
              <button
                type="button"
                onClick={() => setPolicyDays(Math.max(1, policyDays - 1))}
                className="w-11 h-11 rounded-xl border-[1.5px] border-line bg-white text-xl font-bold text-ink"
              >
                –
              </button>
              <div className="text-[32px] font-extrabold min-w-[48px] text-center tracking-tight">
                {policyDays}
              </div>
              <button
                type="button"
                onClick={() => setPolicyDays(Math.min(5, policyDays + 1))}
                className="w-11 h-11 rounded-xl border-[1.5px] border-line bg-white text-xl font-bold text-ink"
              >
                +
              </button>
            </div>
          </div>
        )}

        <div className="bg-white border-[1.5px] border-line rounded-2xl p-5 mb-4">
          <div className="text-[13px] text-muted font-semibold mb-1.5">
            Da quando monitorare
          </div>
          <div className="text-xs text-muted mb-3">
            I giorni richiesti si calcolano da questa data in poi.
          </div>
          <input
            type="date"
            value={monitoringStartDate}
            onChange={(e) => setMonitoringStartDate(e.target.value)}
            className="w-full px-3.5 py-2.5 rounded-xl border-[1.5px] border-line text-sm font-semibold
                       text-ink bg-white outline-none focus:border-ink transition-colors"
          />
        </div>

        {error && <div className="text-xs font-semibold text-pace-red mb-3">{error}</div>}

        <div className="flex gap-2.5">
          <button
            type="button"
            onClick={onClose}
            disabled={saving}
            className="shrink-0 px-[18px] py-4 rounded-2xl border-[1.5px] border-line bg-white font-extrabold text-[15px] text-ink disabled:opacity-50"
          >
            Annulla
          </button>
          <button
            type="button"
            onClick={handleSave}
            disabled={saving}
            className="flex-1 p-4 rounded-2xl border-none font-extrabold text-[15px] text-white bg-ink disabled:opacity-60"
          >
            {saving ? "Salvataggio…" : "Salva"}
          </button>
        </div>
      </div>
    </>
  );
}

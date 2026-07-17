import { calculateAnnualTargetPreview } from "../../lib/planPreview.js";

export default function StepSummary({
  companyName,
  city,
  policyType,
  policyPercent,
  policyDays,
  onBack,
  onFinish,
  submitting,
  submitError,
}) {
  const year = new Date().getFullYear();
  // policyPercent rappresenta la % richiesta in ufficio (coerente con lo step precedente);
  // calculateAnnualTargetPreview si aspetta invece la % di smart working, il complemento a 100.
  const preview = calculateAnnualTargetPreview(
    {
      policyType,
      smartWorkingPercentage: 100 - policyPercent,
      officeDaysPerWeek: policyDays,
      workDaysPerWeek: 5,
    },
    year
  );

  const policySummaryText =
    policyType === "PERCENT" ? `${policyPercent}% in ufficio` : `${policyDays} giorni/settimana`;

  return (
    <div className="flex flex-col flex-1">
      <div className="text-2xl font-extrabold tracking-tight leading-tight mb-2">
        Il tuo obiettivo {year}
      </div>
      <div className="text-sm text-muted leading-relaxed mb-5">
        Verifica il calcolo prima di iniziare.
      </div>

      <div className="bg-ink rounded-[18px] p-[22px] mb-3.5 text-white">
        <div className="text-xs font-bold opacity-65 uppercase tracking-wide mb-1.5">
          Giorni ufficio richiesti / anno
        </div>
        <div className="text-[44px] font-extrabold tracking-tight leading-none">
          {preview.requiredOfficeDays}
        </div>
        <div className="text-[12.5px] opacity-70 mt-1">
          su {preview.totalWorkingDays} giorni lavorativi stimati
        </div>
      </div>

      <div className="flex flex-col gap-2.5 mb-2">
        <SummaryRow label="Azienda" value={companyName || "—"} />
        <SummaryRow label="Sede" value={city || "—"} />
        <SummaryRow label="Policy" value={policySummaryText} />
      </div>

      <div className="flex-1" />

      {submitError && (
        <div className="text-xs font-semibold text-pace-red mb-2">{submitError}</div>
      )}

      <div className="flex gap-2.5">
        <button
          type="button"
          onClick={onBack}
          disabled={submitting}
          className="shrink-0 px-[18px] py-4 rounded-2xl border-[1.5px] border-line bg-surface font-extrabold text-[15px] text-ink disabled:opacity-50"
        >
          Indietro
        </button>
        <button
          type="button"
          onClick={onFinish}
          disabled={submitting}
          className="flex-1 p-4 rounded-2xl border-none font-extrabold text-[15px] text-white bg-ink disabled:opacity-60"
        >
          {submitting ? "Attendere…" : "Inizia a monitorare"}
        </button>
      </div>
    </div>
  );
}

function SummaryRow({ label, value }) {
  return (
    <div className="flex justify-between px-3.5 py-3 bg-surface border-[1.5px] border-line rounded-xl text-[13px]">
      <span className="text-muted font-semibold">{label}</span>
      <span className="font-bold">{value}</span>
    </div>
  );
}

import { useState } from "react";
import { api } from "../../api/client.js";
import { addDays, dateKey, ITA_MONTHS, WD_SHORT } from "../../lib/dateUtils.js";
import { PACE_META, STATUS_DEFS } from "../../lib/statusDefs.js";

const WEEKDAYS = [
  { key: "mon", label: "Lunedì", dow: 1 },
  { key: "tue", label: "Martedì", dow: 2 },
  { key: "wed", label: "Mercoledì", dow: 3 },
  { key: "thu", label: "Giovedì", dow: 4 },
  { key: "fri", label: "Venerdì", dow: 5 },
];

const OFFICE_DEF = STATUS_DEFS[0];
const SMART_DEF = STATUS_DEFS[1];

function buildPlan(pattern, weeks) {
  const entries = [];
  let d = addDays(new Date(), 1);
  d.setHours(0, 0, 0, 0);
  const dayKeyByDow = { 0: null, 1: "mon", 2: "tue", 3: "wed", 4: "thu", 5: "fri", 6: null };

  for (let i = 0; i < weeks * 7; i++) {
    const dow = d.getDay();
    const key = dayKeyByDow[dow];
    if (key && pattern[key]) {
      entries.push({
        date: dateKey(d.getFullYear(), d.getMonth(), d.getDate()),
        type: pattern[key] === "office" ? "OFFICE" : "SMART_WORKING",
      });
    }
    d = addDays(d, 1);
  }
  return entries;
}

export default function Simulation({ year }) {
  const [pattern, setPattern] = useState({
    mon: "office", tue: "smart", wed: "office", thu: "smart", fri: "office",
  });
  const [weeks, setWeeks] = useState(6);
  const [result, setResult] = useState(null);
  const [plan, setPlan] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const setDay = (key, value) => setPattern((p) => ({ ...p, [key]: value }));

  const apply = async () => {
    setLoading(true);
    setError(null);
    try {
      const hypotheticalEntries = buildPlan(pattern, weeks);
      const res = await api.simulate(hypotheticalEntries);
      setResult(res);
      setPlan(hypotheticalEntries);
    } catch {
      setError("Non è stato possibile calcolare la simulazione.");
    } finally {
      setLoading(false);
    }
  };

  const projected = result?.projected;
  const projectedDone = projected?.completed_office_days ?? 0;
  const requiredDays = projected?.required_office_days ?? 0;
  const simProjectedPct = requiredDays > 0 ? Math.min(100, Math.round((projectedDone / requiredDays) * 100)) : 0;

  let simPace = "red";
  if (projectedDone >= requiredDays) simPace = "green";
  else if (projectedDone >= requiredDays * 0.85) simPace = "orange";
  const simMeta = PACE_META[simPace];
  const simBannerLabel =
    simPace === "green"
      ? "Piano sufficiente a raggiungere l'obiettivo"
      : simPace === "orange"
        ? "Piano vicino all'obiettivo, margine ridotto"
        : `Mancherebbero ancora ${Math.max(requiredDays - projectedDone, 0)} giorni`;

  const simEnd = addDays(new Date(), weeks * 7);
  const simEndLabel = `${simEnd.getDate()} ${ITA_MONTHS[simEnd.getMonth()].slice(0, 3)}`;

  const planByDate = new Map(plan.map((p) => [p.date, p.type]));
  const next14 = Array.from({ length: 14 }, (_, i) => {
    const d = addDays(new Date(), i + 1);
    const key = dateKey(d.getFullYear(), d.getMonth(), d.getDate());
    const type = planByDate.get(key);
    const def = type && STATUS_DEFS.find((s) => s.key === type);
    const isWeekend = d.getDay() === 0 || d.getDay() === 6;
    return { key, wd: WD_SHORT[(d.getDay() + 6) % 7], num: d.getDate(), def, isWeekend };
  });

  return (
    <div>
      <div className="text-[12.5px] font-bold text-muted uppercase tracking-wide mb-2.5">
        Settimana tipo
      </div>
      <div className="flex flex-col gap-2 mb-[18px]">
        {WEEKDAYS.map((w) => (
          <div
            key={w.key}
            className="flex items-center justify-between bg-surface border-[1.5px] border-line rounded-xl py-2.5 pl-3.5 pr-2.5"
          >
            <div className="text-[13px] font-bold">{w.label}</div>
            <div className="flex gap-1.5">
              <ToggleButton
                active={pattern[w.key] === "office"}
                def={OFFICE_DEF}
                onClick={() => setDay(w.key, "office")}
              >
                Ufficio
              </ToggleButton>
              <ToggleButton
                active={pattern[w.key] === "smart"}
                def={SMART_DEF}
                onClick={() => setDay(w.key, "smart")}
              >
                Smart
              </ToggleButton>
            </div>
          </div>
        ))}
      </div>

      <div className="flex items-center justify-between bg-surface border-[1.5px] border-line rounded-2xl px-4 py-3.5 mb-[18px]">
        <div className="text-[13px] font-bold">Applica per</div>
        <div className="flex items-center gap-3.5">
          <button
            type="button"
            onClick={() => setWeeks((w) => Math.max(2, w - 1))}
            className="w-[30px] h-[30px] rounded-[9px] border-[1.5px] border-line bg-surface text-base font-bold text-ink"
          >
            –
          </button>
          <div className="text-[15px] font-extrabold min-w-[64px] text-center">{weeks} sett.</div>
          <button
            type="button"
            onClick={() => setWeeks((w) => Math.min(12, w + 1))}
            className="w-[30px] h-[30px] rounded-[9px] border-[1.5px] border-line bg-surface text-base font-bold text-ink"
          >
            +
          </button>
        </div>
      </div>

      <button
        type="button"
        onClick={apply}
        disabled={loading}
        className="w-full py-[15px] rounded-2xl border-none font-extrabold text-[14.5px] text-white bg-office disabled:opacity-60"
      >
        {loading ? "Calcolo…" : "Applica piano di simulazione"}
      </button>

      {error && <div className="text-xs font-semibold text-pace-red mt-2">{error}</div>}

      {result && (
        <>
          <div className="bg-ink rounded-[18px] p-5 my-[18px] text-white">
            <div className="text-xs font-bold opacity-65 uppercase tracking-wide mb-1.5">
              Proiezione al {simEndLabel}
            </div>
            <div className="text-4xl font-extrabold tracking-tight mb-1.5">{simProjectedPct}%</div>
            <div className="flex items-center gap-1.5 mt-1">
              <div className={`w-[7px] h-[7px] rounded-full ${simMeta.bg}`} />
              <div className="text-[13px] font-semibold opacity-90">{simBannerLabel}</div>
            </div>
          </div>

          <div className="text-[12.5px] font-bold text-muted uppercase tracking-wide mb-2.5">
            Prossimi 14 giorni
          </div>
          <div className="grid grid-cols-7 gap-1.5">
            {next14.map((d) => (
              <div
                key={d.key}
                className={`aspect-square rounded-[9px] flex flex-col items-center justify-center
                  ${d.def ? `${d.def.bgSoft} border-[1.5px] border-dashed ${d.def.border}` : "border border-line"}
                  ${d.isWeekend ? "opacity-35" : ""}`}
              >
                <div className="text-[9px] opacity-70">{d.wd}</div>
                <div className="text-xs font-extrabold">{d.num}</div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

function ToggleButton({ active, def, onClick, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`py-[7px] px-3 rounded-[9px] border-[1.5px] text-[11.5px] font-bold
        ${active ? `${def.bg} text-white border-transparent` : "border-line text-muted bg-transparent"}`}
    >
      {children}
    </button>
  );
}

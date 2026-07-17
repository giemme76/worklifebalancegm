import { useSession } from "../../context/SessionContext.jsx";
import { addDays, dateKey, todayKey, WD_SHORT } from "../../lib/dateUtils.js";
import { LINE_COLOR_VALUE, PACE_COLOR_VALUES, PACE_META, STATUS_DEFS } from "../../lib/statusDefs.js";

export default function Dashboard({ year, onOpenSheet }) {
  const { dashboardByYear, calendarByYear, setAttendance, loadingYears } = useSession();
  const dashboard = dashboardByYear[year];
  const calendar = calendarByYear[year];

  if (!dashboard || !calendar) {
    return (
      <div className="flex items-center justify-center py-16 text-muted text-sm">
        {loadingYears[year] ? "Caricamento…" : "—"}
      </div>
    );
  }

  const progressPct =
    dashboard.required_office_days > 0
      ? Math.min(100, Math.round((dashboard.completed_office_days / dashboard.required_office_days) * 100))
      : 0;

  const paceColor = PACE_COLOR_VALUES[dashboard.pace];
  const paceMeta = PACE_META[dashboard.pace];
  const ringStyle = {
    background: `conic-gradient(${paceColor} ${progressPct}%, ${LINE_COLOR_VALUE} ${progressPct}% 100%)`,
  };

  const today = todayKey();
  const todayEntry = calendar.entries.find((e) => e.date === today);

  const recentDays = Array.from({ length: 7 }, (_, i) => {
    const d = addDays(new Date(), -(6 - i));
    const key = dateKey(d.getFullYear(), d.getMonth(), d.getDate());
    const entry = calendar.entries.find((e) => e.date === key);
    const def = entry && STATUS_DEFS.find((s) => s.key === entry.type);
    return { key, wd: WD_SHORT[(d.getDay() + 6) % 7], num: d.getDate(), def };
  });

  const breakdown = [
    { label: "Smart working", count: calendar.counts.smart_working, def: STATUS_DEFS[1] },
    { label: "Ferie", count: calendar.counts.vacation, def: STATUS_DEFS[2] },
    { label: "Permessi", count: calendar.counts.permit, def: STATUS_DEFS[3] },
    { label: "Malattia", count: calendar.counts.sick, def: STATUS_DEFS[4] },
    { label: "Trasferta", count: calendar.counts.travel, def: STATUS_DEFS[5] },
  ];

  return (
    <div>
      <div className="flex flex-col items-center bg-surface border-[1.5px] border-line rounded-[20px] px-5 py-[26px] mb-4">
        <div
          className="w-[150px] h-[150px] rounded-full flex items-center justify-center mb-4"
          style={ringStyle}
        >
          <div className="w-[112px] h-[112px] rounded-full bg-surface flex flex-col items-center justify-center">
            <div className="text-[30px] font-extrabold tracking-tight">{progressPct}%</div>
            <div className="text-[11px] text-muted font-semibold">completato</div>
          </div>
        </div>
        <div className={`flex items-center gap-1.5 px-3.5 py-2 rounded-full ${paceMeta.bgSoft}`}>
          <div className={`w-[7px] h-[7px] rounded-full ${paceMeta.bg}`} />
          <div className={`text-[12.5px] font-bold ${paceMeta.text}`}>{dashboard.pace_label}</div>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-2.5 mb-[18px]">
        <StatBox value={dashboard.completed_office_days} label="Fatti" />
        <StatBox value={dashboard.required_office_days} label="Richiesti" />
        <StatBox value={dashboard.missing_office_days} label="Rimanenti" />
      </div>

      <SectionLabel>Registra oggi</SectionLabel>
      <div className="grid grid-cols-3 gap-2 mb-5">
        {STATUS_DEFS.map((s) => {
          const active = todayEntry?.type === s.key;
          return (
            <button
              key={s.key}
              type="button"
              onClick={() => setAttendance(today, s.key)}
              className={`py-3 px-1.5 rounded-xl border-[1.5px] text-[11.5px] font-bold transition-colors
                ${active ? `${s.bg} text-white border-transparent` : `bg-surface border-line text-ink`}`}
            >
              {s.label}
            </button>
          );
        })}
      </div>

      <SectionLabel>Questa settimana</SectionLabel>
      <div className="flex gap-1.5 mb-5">
        {recentDays.map((d) => (
          <button
            key={d.key}
            type="button"
            onClick={() => onOpenSheet(d.key)}
            className={`flex-1 py-2 rounded-[10px] border-[1.5px] flex flex-col items-center gap-0.5
              ${d.key === today ? "border-ink" : "border-line"}
              ${d.def ? `${d.def.bg} text-white border-transparent` : "bg-surface text-ink"}`}
          >
            <div className="text-[9.5px] opacity-75">{d.wd}</div>
            <div className="text-[13px] font-extrabold">{d.num}</div>
          </button>
        ))}
      </div>

      <SectionLabel>Riepilogo assenze</SectionLabel>
      <div className="grid grid-cols-2 gap-2">
        {breakdown.map((b) => (
          <div
            key={b.label}
            className="flex items-center gap-2 bg-surface border-[1.5px] border-line rounded-xl px-3 py-[11px]"
          >
            <div className={`w-[9px] h-[9px] rounded-full ${b.def.dot} shrink-0`} />
            <div className="text-[12.5px] font-semibold flex-1">{b.label}</div>
            <div className="text-sm font-extrabold">{b.count}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function StatBox({ value, label }) {
  return (
    <div className="bg-surface border-[1.5px] border-line rounded-2xl py-3.5 px-2.5 text-center">
      <div className="text-xl font-extrabold">{value}</div>
      <div className="text-[10.5px] text-muted font-semibold mt-0.5">{label}</div>
    </div>
  );
}

function SectionLabel({ children }) {
  return (
    <div className="text-[12.5px] font-bold text-muted uppercase tracking-wide mb-2.5">
      {children}
    </div>
  );
}

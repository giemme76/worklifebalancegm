import { useEffect, useState } from "react";
import { useSession } from "../../context/SessionContext.jsx";
import { buildMonthGrid, ITA_MONTHS, shiftMonth, todayKey, WD_SHORT } from "../../lib/dateUtils.js";
import { STATUS_DEFS } from "../../lib/statusDefs.js";

export default function CalendarView({ onOpenSheet }) {
  const { calendarByYear, refreshYear, loadingYears } = useSession();
  const now = new Date();
  const [calYear, setCalYear] = useState(now.getFullYear());
  const [calMonth, setCalMonth] = useState(now.getMonth());

  useEffect(() => {
    if (!calendarByYear[calYear]) refreshYear(calYear);
  }, [calYear, calendarByYear, refreshYear]);

  const calendar = calendarByYear[calYear];
  const entriesByDate = new Map((calendar?.entries || []).map((e) => [e.date, e]));
  const today = todayKey();

  const weeks = buildMonthGrid(calYear, calMonth);

  const goPrev = () => {
    const { year, month } = shiftMonth(calYear, calMonth, -1);
    setCalYear(year);
    setCalMonth(month);
  };
  const goNext = () => {
    const { year, month } = shiftMonth(calYear, calMonth, 1);
    setCalYear(year);
    setCalMonth(month);
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <NavArrow onClick={goPrev} label="Mese precedente">
          ‹
        </NavArrow>
        <div className="text-[15px] font-extrabold">
          {ITA_MONTHS[calMonth]} {calYear}
        </div>
        <NavArrow onClick={goNext} label="Mese successivo">
          ›
        </NavArrow>
      </div>

      <div className="grid grid-cols-7 gap-1 mb-1.5">
        {WD_SHORT.map((wl, i) => (
          <div key={i} className="text-center text-[10.5px] font-bold text-muted">
            {wl}
          </div>
        ))}
      </div>

      {loadingYears[calYear] && !calendar ? (
        <div className="text-center text-sm text-muted py-10">Caricamento…</div>
      ) : (
        weeks.map((week, wi) => (
          <div key={wi} className="grid grid-cols-7 gap-1 mb-1">
            {week.map((cell, ci) => {
              if (!cell) return <div key={ci} className="aspect-square invisible" />;
              const entry = entriesByDate.get(cell.key);
              const def = entry && STATUS_DEFS.find((s) => s.key === entry.type);
              const isToday = cell.key === today;
              return (
                <button
                  key={cell.key}
                  type="button"
                  onClick={() => onOpenSheet(cell.key)}
                  className={`aspect-square rounded-[10px] text-[13px] font-bold flex items-center justify-center border-[1.5px]
                    ${def ? `${def.bg} text-white border-transparent` : "text-ink border-transparent"}
                    ${!def && isToday ? "border-ink" : ""}`}
                >
                  {cell.day}
                </button>
              );
            })}
          </div>
        ))
      )}

      <div className="flex flex-wrap gap-2.5 mt-4">
        {STATUS_DEFS.map((s) => (
          <div key={s.key} className="flex items-center gap-1.5">
            <div className={`w-2 h-2 rounded-full ${s.dot}`} />
            <div className="text-[11px] font-semibold text-muted">{s.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function NavArrow({ onClick, children, label }) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={label}
      className="w-8 h-8 rounded-[9px] border-[1.5px] border-line bg-surface text-base font-bold text-ink"
    >
      {children}
    </button>
  );
}

import { useState } from "react";
import { useSession } from "../../context/SessionContext.jsx";
import { ITA_DAYS, ITA_MONTHS, parseDateKey } from "../../lib/dateUtils.js";
import { STATUS_DEFS } from "../../lib/statusDefs.js";

export default function BottomSheet({ dateStr, onClose }) {
  const { entryForDate, setAttendance, removeAttendance } = useSession();
  const [busy, setBusy] = useState(false);

  const entry = entryForDate(dateStr);
  const d = parseDateKey(dateStr);
  const label = `${ITA_DAYS[d.getDay()]} ${d.getDate()} ${ITA_MONTHS[d.getMonth()]}`;

  const pick = async (statusKey) => {
    setBusy(true);
    try {
      await setAttendance(dateStr, statusKey);
      onClose();
    } finally {
      setBusy(false);
    }
  };

  const clear = async () => {
    setBusy(true);
    try {
      await removeAttendance(dateStr);
      onClose();
    } finally {
      setBusy(false);
    }
  };

  return (
    <>
      <div
        onClick={onClose}
        className="absolute inset-0 bg-black/40 z-10 animate-wl-fade"
      />
      <div
        className="absolute left-0 right-0 bottom-0 bg-surface rounded-t-[22px] px-5 z-20 animate-wl-sheet-up"
        style={{ paddingTop: 18, paddingBottom: "calc(22px + env(safe-area-inset-bottom, 0px))" }}
      >
        <div className="w-9 h-1 rounded-full bg-line mx-auto mb-4" />
        <div className="text-[15px] font-extrabold mb-3.5">{label}</div>

        <div className="grid grid-cols-2 gap-2 mb-2.5">
          {STATUS_DEFS.map((s) => {
            const active = entry?.type === s.key;
            return (
              <button
                key={s.key}
                type="button"
                disabled={busy}
                onClick={() => pick(s.key)}
                className={`py-3.5 px-2 rounded-xl border-[1.5px] text-[13px] font-bold flex items-center gap-2 justify-start pl-3.5
                  ${active ? `${s.bg} text-white border-transparent` : "bg-surface border-line text-ink"}`}
              >
                {s.label}
              </button>
            );
          })}
        </div>

        {entry && (
          <button
            type="button"
            disabled={busy}
            onClick={clear}
            className="w-full py-3 border-none bg-transparent text-muted text-[13px] font-bold"
          >
            Rimuovi registrazione
          </button>
        )}
      </div>
    </>
  );
}

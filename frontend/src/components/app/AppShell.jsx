import { useEffect, useState } from "react";
import { useSession } from "../../context/SessionContext.jsx";
import logo from "../../img/worklife-logo-header.png";
import BottomSheet from "./BottomSheet.jsx";
import CalendarView from "./CalendarView.jsx";
import Dashboard from "./Dashboard.jsx";
import SessionInfoSheet from "./SessionInfoSheet.jsx";
import Simulation from "./Simulation.jsx";

const NICKNAME_BADGE_MAX_LENGTH = 10;

export default function AppShell() {
  const { session, refreshYear } = useSession();
  const [tab, setTab] = useState("dashboard");
  const [sheetDate, setSheetDate] = useState(null);
  const [showSessionInfo, setShowSessionInfo] = useState(false);

  const year = new Date().getFullYear();

  useEffect(() => {
    refreshYear(year);
  }, [refreshYear, year]);

  const company = session?.company;
  const nickname = session?.nickname;
  const initials = (company?.name || "WL").slice(0, 2).toUpperCase();
  const badgeLabel = (nickname || initials).slice(0, NICKNAME_BADGE_MAX_LENGTH);

  return (
    <div className="flex flex-col h-full overflow-hidden relative">
      <div className="shrink-0 px-5 pt-[18px] pb-3 flex items-center justify-between border-b border-line">
        <img src={logo} alt="WorkLifeBalanceGM" className="h-8 w-auto" />
        <button
          type="button"
          onClick={() => setShowSessionInfo(true)}
          className="max-w-[110px] h-[34px] px-3 rounded-[10px] bg-office-soft flex items-center
                     justify-center text-xs font-extrabold text-office truncate border-none cursor-pointer"
          title={nickname || undefined}
        >
          {badgeLabel}
        </button>
      </div>

      <div className="flex-1 overflow-y-auto px-5 pt-[18px] pb-6">
        {tab === "dashboard" && <Dashboard year={year} onOpenSheet={setSheetDate} />}
        {tab === "calendar" && <CalendarView onOpenSheet={setSheetDate} />}
        {tab === "simulation" && <Simulation year={year} />}
      </div>

      <div
        className="shrink-0 flex border-t border-line bg-surface px-2.5 pt-2"
        style={{ paddingBottom: "calc(6px + env(safe-area-inset-bottom, 0px))" }}
      >
        <TabButton active={tab === "dashboard"} label="Dashboard" onClick={() => setTab("dashboard")}>
          <div className="grid grid-cols-2 gap-0.5 w-3.5 h-3.5">
            <div className={`rounded-sm ${tab === "dashboard" ? "bg-ink" : "bg-muted"}`} />
            <div className={`rounded-sm ${tab === "dashboard" ? "bg-ink" : "bg-muted"}`} />
            <div className={`rounded-sm ${tab === "dashboard" ? "bg-ink" : "bg-muted"}`} />
            <div className={`rounded-sm ${tab === "dashboard" ? "bg-ink" : "bg-muted"}`} />
          </div>
        </TabButton>
        <TabButton active={tab === "calendar"} label="Calendario" onClick={() => setTab("calendar")}>
          <div className="w-[15px] h-3.5 border-[1.6px] border-current rounded-sm relative">
            <div className="absolute -top-[1.6px] -left-[1.6px] -right-[1.6px] h-[3.5px] rounded-t-sm bg-current" />
          </div>
        </TabButton>
        <TabButton
          active={tab === "simulation"}
          label="Simulazione"
          onClick={() => setTab("simulation")}
        >
          <div className="flex items-end gap-0.5 h-3.5">
            <div className="w-[3px] h-1.5 bg-current rounded-sm" />
            <div className="w-[3px] h-3.5 bg-current rounded-sm" />
            <div className="w-[3px] h-2.5 bg-current rounded-sm" />
          </div>
        </TabButton>
      </div>

      {sheetDate && <BottomSheet dateStr={sheetDate} onClose={() => setSheetDate(null)} />}
      {showSessionInfo && <SessionInfoSheet onClose={() => setShowSessionInfo(false)} />}
    </div>
  );
}

function TabButton({ active, label, onClick, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`flex-1 flex flex-col items-center gap-1 py-1.5 px-1 border-none bg-transparent text-[9.5px] font-bold
                  ${active ? "text-ink" : "text-muted"}`}
    >
      {children}
      <div>{label}</div>
    </button>
  );
}

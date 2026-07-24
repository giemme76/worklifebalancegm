import { useEffect, useState } from "react";
import { useSession } from "../../context/SessionContext.jsx";
import BrandWordmark from "../BrandWordmark.jsx";
import BottomSheet from "./BottomSheet.jsx";
import CalendarView from "./CalendarView.jsx";
import CompanySettingsSheet from "./CompanySettingsSheet.jsx";
import Dashboard from "./Dashboard.jsx";
import SessionInfoSheet from "./SessionInfoSheet.jsx";
import Simulation from "./Simulation.jsx";

const NICKNAME_BADGE_MAX_LENGTH = 10;

export default function AppShell() {
  const { session, refreshYear } = useSession();
  const [tab, setTab] = useState("dashboard");
  const [sheetDate, setSheetDate] = useState(null);
  const [showSessionInfo, setShowSessionInfo] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

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
        <BrandWordmark className="text-base" />
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setShowSettings(true)}
            aria-label="Impostazioni"
            title="Impostazioni"
            className="w-[34px] h-[34px] rounded-[10px] bg-surface border-[1.5px] border-line
                       flex items-center justify-center text-ink cursor-pointer"
          >
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="12" cy="12" r="3" />
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
            </svg>
          </button>
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
      {showSettings && <CompanySettingsSheet onClose={() => setShowSettings(false)} />}
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

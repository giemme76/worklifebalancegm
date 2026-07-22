import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { api, ApiError } from "../api/client.js";

const SessionContext = createContext(null);

export function SessionProvider({ children }) {
  // 'loading' | 'onboarding' | 'welcome' | 'app'
  const [status, setStatus] = useState("loading");
  const [session, setSession] = useState(null);
  const [error, setError] = useState(null);

  const [dashboardByYear, setDashboardByYear] = useState({});
  const [calendarByYear, setCalendarByYear] = useState({});
  const [loadingYears, setLoadingYears] = useState({});

  // Bootstrap: c'è già una sessione valida nel cookie del browser?
  useEffect(() => {
    let cancelled = false;
    api
      .getCurrentSession()
      .then((data) => {
        if (cancelled) return;
        setSession(data);
        setStatus("app");
      })
      .catch((err) => {
        if (cancelled) return;
        if (err instanceof ApiError && err.status === 401) {
          setStatus("onboarding");
        } else {
          setError("Impossibile contattare il server. Riprova più tardi.");
          setStatus("onboarding");
        }
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const refreshYear = useCallback(async (year) => {
    setLoadingYears((s) => ({ ...s, [year]: true }));
    try {
      const [dashboard, calendar] = await Promise.all([
        api.getDashboard(year),
        api.getCalendar(year),
      ]);
      setDashboardByYear((s) => ({ ...s, [year]: dashboard }));
      setCalendarByYear((s) => ({ ...s, [year]: calendar }));
      return { dashboard, calendar };
    } finally {
      setLoadingYears((s) => ({ ...s, [year]: false }));
    }
  }, []);

  const completeOnboarding = useCallback(async (companySetup) => {
    const created = await api.createSession(companySetup);
    setSession(created);
    // Prima di entrare nell'app mostriamo il codice di recupero: è l'unica
    // occasione in cui l'utente lo vede, e senza salvarlo non c'è modo di
    // recuperare i dati se il cookie di sessione scade o cambia dispositivo.
    setStatus("welcome");
    return created;
  }, []);

  const enterApp = useCallback(() => setStatus("app"), []);

  const recoverSession = useCallback(async (code) => {
    const recovered = await api.recoverSession(code);
    setSession(recovered);
    setStatus("app");
    return recovered;
  }, []);

  const setAttendance = useCallback(
    async (dateStr, type) => {
      const year = Number(dateStr.slice(0, 4));
      await api.createAttendance(dateStr, type);
      await refreshYear(year);
    },
    [refreshYear]
  );

  const removeAttendance = useCallback(
    async (dateStr) => {
      const year = Number(dateStr.slice(0, 4));
      await api.deleteAttendance(dateStr);
      await refreshYear(year);
    },
    [refreshYear]
  );

  const entryForDate = useCallback(
    (dateStr) => {
      const year = Number(dateStr.slice(0, 4));
      const cal = calendarByYear[year];
      if (!cal) return undefined;
      return cal.entries.find((e) => e.date === dateStr);
    },
    [calendarByYear]
  );

  const value = useMemo(
    () => ({
      status,
      session,
      error,
      dashboardByYear,
      calendarByYear,
      loadingYears,
      refreshYear,
      completeOnboarding,
      enterApp,
      recoverSession,
      setAttendance,
      removeAttendance,
      entryForDate,
    }),
    [
      status,
      session,
      error,
      dashboardByYear,
      calendarByYear,
      loadingYears,
      refreshYear,
      completeOnboarding,
      enterApp,
      recoverSession,
      setAttendance,
      removeAttendance,
      entryForDate,
    ]
  );

  return <SessionContext.Provider value={value}>{children}</SessionContext.Provider>;
}

export function useSession() {
  const ctx = useContext(SessionContext);
  if (!ctx) throw new Error("useSession deve essere usato dentro <SessionProvider>");
  return ctx;
}

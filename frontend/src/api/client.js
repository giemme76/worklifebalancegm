const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

/** Errore applicativo con status HTTP e payload del backend allegati. */
export class ApiError extends Error {
  constructor(status, payload) {
    super((payload && payload.detail) || `Richiesta fallita (${status})`);
    this.status = status;
    this.payload = payload;
  }
}

async function request(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (response.status === 204) return null;

  const isJson = response.headers.get("content-type")?.includes("application/json");
  const payload = isJson ? await response.json().catch(() => null) : null;

  if (!response.ok) {
    throw new ApiError(response.status, payload);
  }
  return payload;
}

export const api = {
  // Sessione
  getCurrentSession: () => request("/session"),
  createSession: (data) => request("/session", { method: "POST", body: JSON.stringify(data) }),
  recoverSession: (code) => request(`/session/${encodeURIComponent(code)}`),

  // Dashboard
  getDashboard: (year) => request(`/dashboard?year=${year}`),

  // Calendario
  getCalendar: (year) => request(`/calendar?year=${year}`),

  // Presenze
  createAttendance: (date, type) =>
    request("/attendance", { method: "POST", body: JSON.stringify({ date, type }) }),
  deleteAttendance: (date) => request(`/attendance/${date}`, { method: "DELETE" }),

  // Simulazione
  simulate: (hypotheticalEntries) =>
    request("/simulation", {
      method: "POST",
      body: JSON.stringify({ hypothetical_entries: hypotheticalEntries }),
    }),
};

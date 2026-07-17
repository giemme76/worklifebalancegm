export const ITA_MONTHS = [
  "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
  "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre",
];

export const ITA_DAYS = [
  "Domenica", "Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato",
];

// Lunedì-first, come nel design.
export const WD_SHORT = ["L", "M", "M", "G", "V", "S", "D"];

export function pad2(n) {
  return String(n).padStart(2, "0");
}

/** Chiave data locale YYYY-MM-DD, senza fusi orari (coerente con il campo `date` del backend). */
export function dateKey(year, monthIndex, day) {
  return `${year}-${pad2(monthIndex + 1)}-${pad2(day)}`;
}

export function todayKey() {
  const t = new Date();
  return dateKey(t.getFullYear(), t.getMonth(), t.getDate());
}

export function parseDateKey(key) {
  const [y, m, d] = key.split("-").map(Number);
  return new Date(y, m - 1, d);
}

export function addDays(date, amount) {
  const d = new Date(date);
  d.setDate(d.getDate() + amount);
  return d;
}

/** Indice weekday lunedì-first (0=lunedì ... 6=domenica), a differenza di Date#getDay (0=domenica). */
export function mondayFirstWeekday(date) {
  return (date.getDay() + 6) % 7;
}

/**
 * Costruisce la griglia (settimane x giorni) di un mese, lunedì-first,
 * con celle vuote (null) per completare le settimane iniziale/finale.
 */
export function buildMonthGrid(year, month) {
  const first = new Date(year, month, 1);
  const offset = mondayFirstWeekday(first);
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const cells = [];
  for (let i = 0; i < offset; i++) cells.push(null);
  for (let d = 1; d <= daysInMonth; d++) {
    cells.push({ key: dateKey(year, month, d), day: d });
  }
  while (cells.length % 7 !== 0) cells.push(null);

  const weeks = [];
  for (let i = 0; i < cells.length; i += 7) weeks.push(cells.slice(i, i + 7));
  return weeks;
}

export function shiftMonth(year, month, delta) {
  let m = month + delta;
  let y = year;
  while (m < 0) {
    m += 12;
    y -= 1;
  }
  while (m > 11) {
    m -= 12;
    y += 1;
  }
  return { year: y, month: m };
}

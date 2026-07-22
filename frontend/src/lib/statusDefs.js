// Le 6 tipologie di presenza, allineate all'enum AttendanceType del backend
// e alle classi Tailwind definite in tailwind.config.js (office/smart/vacation/permit/sick/travel).
// Le classi sono scritte per esteso (non interpolate) così Tailwind le trova in fase di scan.
export const STATUS_DEFS = [
  {
    key: "OFFICE",
    label: "Ufficio",
    bg: "bg-office",
    bgSoft: "bg-office-soft",
    text: "text-office",
    border: "border-office",
    dot: "bg-office",
  },
  {
    key: "SMART_WORKING",
    label: "Smart working",
    bg: "bg-smart",
    bgSoft: "bg-smart-soft",
    text: "text-smart",
    border: "border-smart",
    dot: "bg-smart",
  },
  {
    key: "VACATION",
    label: "Ferie",
    bg: "bg-vacation",
    bgSoft: "bg-vacation-soft",
    text: "text-vacation",
    border: "border-vacation",
    dot: "bg-vacation",
  },
  {
    key: "PERMIT",
    label: "Permesso",
    bg: "bg-permit",
    bgSoft: "bg-permit-soft",
    text: "text-permit",
    border: "border-permit",
    dot: "bg-permit",
  },
  {
    key: "SICK",
    label: "Malattia",
    bg: "bg-sick",
    bgSoft: "bg-sick-soft",
    text: "text-sick",
    border: "border-sick",
    dot: "bg-sick",
  },
  {
    key: "TRAVEL",
    label: "Trasferta",
    bg: "bg-travel",
    bgSoft: "bg-travel-soft",
    text: "text-travel",
    border: "border-travel",
    dot: "bg-travel",
  },
];

export const STATUS_BY_KEY = Object.fromEntries(STATUS_DEFS.map((s) => [s.key, s]));

// Semaforo di andamento (pace) restituito da GET /dashboard e POST /simulation.
export const PACE_META = {
  green: { bg: "bg-pace-green", bgSoft: "bg-pace-green-soft", text: "text-pace-green" },
  orange: { bg: "bg-pace-orange", bgSoft: "bg-pace-orange-soft", text: "text-pace-orange" },
  red: { bg: "bg-pace-red", bgSoft: "bg-pace-red-soft", text: "text-pace-red" },
};

// Stessi valori oklch di tailwind.config.js, per gli usi che richiedono un valore CSS
// letterale (es. conic-gradient inline), dove le classi Tailwind non bastano.
export const PACE_COLOR_VALUES = {
  green: "oklch(0.50 0.08 151)",
  orange: "oklch(0.68 0.14 55)",
  red: "oklch(0.58 0.16 25)",
};
export const LINE_COLOR_VALUE = "oklch(0.9 0.008 70)";

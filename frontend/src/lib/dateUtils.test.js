import { describe, expect, it } from "vitest";
import {
  addDays,
  buildMonthGrid,
  dateKey,
  mondayFirstWeekday,
  parseDateKey,
  shiftMonth,
} from "./dateUtils.js";

describe("dateUtils", () => {
  it("dateKey formatta YYYY-MM-DD con zero padding", () => {
    expect(dateKey(2026, 0, 5)).toBe("2026-01-05");
    expect(dateKey(2026, 11, 31)).toBe("2026-12-31");
  });

  it("parseDateKey è l'inverso di dateKey (data locale)", () => {
    const d = parseDateKey("2026-10-02");
    expect([d.getFullYear(), d.getMonth(), d.getDate()]).toEqual([2026, 9, 2]);
  });

  it("addDays scavalca mese e anno senza mutare l'originale", () => {
    const start = new Date(2026, 11, 31);
    const next = addDays(start, 1);
    expect(dateKey(next.getFullYear(), next.getMonth(), next.getDate())).toBe("2027-01-01");
    expect(start.getDate()).toBe(31);
  });

  it("mondayFirstWeekday: lunedì=0, domenica=6", () => {
    expect(mondayFirstWeekday(new Date(2026, 9, 5))).toBe(0); // lunedì 5/10/2026
    expect(mondayFirstWeekday(new Date(2026, 9, 4))).toBe(6); // domenica
  });

  it("buildMonthGrid: settimane da 7, celle vuote iniziali (ottobre 2026 inizia di giovedì)", () => {
    const weeks = buildMonthGrid(2026, 9);
    expect(weeks.every((w) => w.length === 7)).toBe(true);
    expect(weeks[0].slice(0, 3)).toEqual([null, null, null]);
    expect(weeks[0][3]).toEqual({ key: "2026-10-01", day: 1 });
    expect(weeks.flat().filter(Boolean)).toHaveLength(31);
  });

  it("shiftMonth gestisce il cambio anno in entrambe le direzioni", () => {
    expect(shiftMonth(2026, 11, 1)).toEqual({ year: 2027, month: 0 });
    expect(shiftMonth(2026, 0, -1)).toEqual({ year: 2025, month: 11 });
    expect(shiftMonth(2026, 5, 14)).toEqual({ year: 2027, month: 7 });
  });
});

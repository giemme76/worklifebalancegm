import { describe, expect, it } from "vitest";
import {
  calculateAnnualTargetPreview,
  countWorkingDaysInRange,
  countWorkingDaysInYear,
} from "./planPreview.js";

describe("countWorkingDaysInYear", () => {
  it("2026 ha 261 giorni lavorativi lun-ven", () => {
    expect(countWorkingDaysInYear(2026, 5)).toBe(261);
  });

  it("con 7 giorni a settimana coincide con i giorni dell'anno", () => {
    expect(countWorkingDaysInYear(2026, 7)).toBe(365);
    expect(countWorkingDaysInYear(2028, 7)).toBe(366);
  });
});

describe("countWorkingDaysInRange", () => {
  it("estremi inclusi", () => {
    // lun 5/10 - ven 9/10/2026
    expect(countWorkingDaysInRange(new Date(2026, 9, 5), new Date(2026, 9, 9), 5)).toBe(5);
  });

  it("intervallo invertito = 0", () => {
    expect(countWorkingDaysInRange(new Date(2026, 9, 9), new Date(2026, 9, 5), 5)).toBe(0);
  });
});

describe("calculateAnnualTargetPreview", () => {
  const percent = (extra = {}) => ({
    policyType: "PERCENT",
    smartWorkingPercentage: 40,
    workDaysPerWeek: 5,
    ...extra,
  });

  it("policy a percentuale: 60% in ufficio su 261 giorni", () => {
    const r = calculateAnnualTargetPreview(percent(), 2026);
    expect(r.totalWorkingDays).toBe(261);
    expect(r.requiredOfficeDays).toBe(Math.round(261 * 0.6));
    expect(r.requiredSmartDays).toBe(261 - r.requiredOfficeDays);
  });

  it("policy a giorni fissi: 3 giorni/settimana", () => {
    const r = calculateAnnualTargetPreview(
      { policyType: "FIXED_DAYS", officeDaysPerWeek: 3, workDaysPerWeek: 5 },
      2026
    );
    expect(r.requiredOfficeDays).toBe(Math.round(3 * (261 / 5)));
  });

  it("i giorni in ufficio non superano mai i lavorativi", () => {
    const r = calculateAnnualTargetPreview(percent({ smartWorkingPercentage: 0 }), 2026);
    expect(r.requiredOfficeDays).toBe(r.totalWorkingDays);
    expect(r.requiredSmartDays).toBe(0);
  });

  it("una data di inizio a metà anno riduce il totale", () => {
    const full = calculateAnnualTargetPreview(percent(), 2026);
    const partial = calculateAnnualTargetPreview(percent({ monitoringStartDate: "2026-10-01" }), 2026);
    expect(partial.totalWorkingDays).toBeGreaterThan(0);
    expect(partial.totalWorkingDays).toBeLessThan(full.totalWorkingDays);
  });

  it("inizio in un anno futuro = obiettivo zero", () => {
    const r = calculateAnnualTargetPreview(percent({ monitoringStartDate: "2027-01-01" }), 2026);
    expect(r).toEqual({ totalWorkingDays: 0, requiredOfficeDays: 0, requiredSmartDays: 0 });
  });
});

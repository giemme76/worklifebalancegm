// Stima lato client dell'obiettivo annuale, usata solo per l'anteprima nello step 3
// dell'onboarding (prima ancora che esista una sessione). La stessa logica di
// app/utils/date_utils.py e app/services/calculation_service.py sul backend,
// così l'anteprima coincide con quanto la dashboard mostrerà subito dopo.

export function countWorkingDaysInYear(year, workDaysPerWeek = 5) {
  return countWorkingDaysInRange(new Date(year, 0, 1), new Date(year, 11, 31), workDaysPerWeek);
}

export function countWorkingDaysInRange(start, end, workDaysPerWeek = 5) {
  if (start > end) return 0;
  const validWeekdays = new Set(
    Array.from({ length: Math.max(1, Math.min(workDaysPerWeek, 7)) }, (_, i) => i)
  );
  // getDay(): 0=domenica..6=sabato. Convertiamo a lunedì-first (0=lunedì..6=domenica).
  let count = 0;
  const d = new Date(start);
  while (d <= end) {
    const mondayFirst = (d.getDay() + 6) % 7;
    if (validWeekdays.has(mondayFirst)) count++;
    d.setDate(d.getDate() + 1);
  }
  return count;
}

export function calculateAnnualTargetPreview(
  { policyType, smartWorkingPercentage, officeDaysPerWeek, workDaysPerWeek = 5, monitoringStartDate },
  year
) {
  const yearStart = new Date(year, 0, 1);
  const yearEnd = new Date(year, 11, 31);
  let effectiveStart = yearStart;
  if (monitoringStartDate) {
    const start = new Date(`${monitoringStartDate}T00:00:00`);
    if (start.getFullYear() > year) {
      // Il monitoraggio non è ancora iniziato in quest'anno: nessun obiettivo attivo.
      return { totalWorkingDays: 0, requiredOfficeDays: 0, requiredSmartDays: 0 };
    }
    if (start.getFullYear() === year) effectiveStart = start;
  }

  const totalWorkingDays = countWorkingDaysInRange(effectiveStart, yearEnd, workDaysPerWeek);

  let requiredOfficeDays;
  if (policyType === "FIXED_DAYS") {
    const workingWeeks = totalWorkingDays / workDaysPerWeek;
    requiredOfficeDays = Math.round((officeDaysPerWeek || 0) * workingWeeks);
  } else {
    const officePercentage = 100 - (smartWorkingPercentage ?? 0);
    requiredOfficeDays = Math.round((totalWorkingDays * officePercentage) / 100);
  }
  requiredOfficeDays = Math.min(requiredOfficeDays, totalWorkingDays);

  return { totalWorkingDays, requiredOfficeDays, requiredSmartDays: totalWorkingDays - requiredOfficeDays };
}

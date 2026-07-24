import { useState } from "react";
import { useSession } from "../../context/SessionContext.jsx";
import BrandWordmark from "../BrandWordmark.jsx";
import StepCompany from "./StepCompany.jsx";
import StepPolicy from "./StepPolicy.jsx";
import StepSummary from "./StepSummary.jsx";

export default function OnboardingFlow() {
  const { completeOnboarding, recoverSession } = useSession();

  const [step, setStep] = useState(1);
  const [nickname, setNickname] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [detected, setDetected] = useState(false);
  const [city, setCity] = useState("");

  const [policyType, setPolicyType] = useState("PERCENT");
  const [policyPercent, setPolicyPercent] = useState(60);
  const [policyDays, setPolicyDays] = useState(3);

  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);

  const [showRecovery, setShowRecovery] = useState(false);
  const [recoveryCode, setRecoveryCode] = useState("");
  const [recovering, setRecovering] = useState(false);
  const [recoveryError, setRecoveryError] = useState(null);

  const handleRecover = async () => {
    const code = recoveryCode.trim();
    if (!code) return;
    setRecovering(true);
    setRecoveryError(null);
    try {
      await recoverSession(code);
    } catch {
      setRecoveryError("Codice non trovato. Controlla di averlo copiato correttamente.");
      setRecovering(false);
    }
  };

  const finishOnboarding = async () => {
    setSubmitting(true);
    setSubmitError(null);
    try {
      await completeOnboarding({
        nickname: nickname.trim() || undefined,
        name: companyName.trim(),
        headquarters: city || undefined,
        policy_type: policyType,
        // policyPercent nella UI rappresenta la % richiesta in ufficio (coerente col design);
        // il backend si aspetta invece la % di smart working, cioè il suo complemento a 100.
        smart_working_percentage: policyType === "PERCENT" ? 100 - policyPercent : undefined,
        office_days_per_week: policyType === "FIXED_DAYS" ? policyDays : undefined,
        work_days_per_week: 5,
      });
    } catch (err) {
      setSubmitError("Non è stato possibile creare la sessione. Riprova.");
      setSubmitting(false);
    }
  };

  return (
    <div className="flex flex-col h-full px-[22px] py-6 overflow-y-auto">
      <div className="flex items-center justify-between mb-7">
        <BrandWordmark className="text-2xl" />
        {step === 1 && !showRecovery && (
          <button
            type="button"
            onClick={() => setShowRecovery(true)}
            className="border-none bg-transparent text-xs font-bold text-office cursor-pointer px-1"
          >
            Ho già un codice
          </button>
        )}
      </div>

      {step === 1 && showRecovery && (
        <div className="flex flex-col gap-2 px-4 py-3.5 rounded-2xl bg-surface border-[1.5px] border-line mb-6">
          <div className="text-[13px] font-bold">Recupera la tua sessione</div>
          <div className="text-xs text-muted mb-1">Inserisci il codice ricevuto alla creazione (es. SW-XXXX-XXXX)</div>
          <input
            type="text"
            placeholder="SW-XXXX-XXXX"
            value={recoveryCode}
            onChange={(e) => setRecoveryCode(e.target.value)}
            className="w-full px-3.5 py-2.5 rounded-xl border-[1.5px] border-line text-sm font-semibold
                       text-ink bg-white outline-none focus:border-ink transition-colors font-mono"
          />
          {recoveryError && <div className="text-xs font-semibold text-pace-red">{recoveryError}</div>}
          <div className="flex gap-2 mt-1">
            <button
              type="button"
              onClick={() => {
                setShowRecovery(false);
                setRecoveryError(null);
              }}
              disabled={recovering}
              className="shrink-0 px-3.5 py-2.5 rounded-xl border-[1.5px] border-line bg-surface font-bold text-xs text-ink disabled:opacity-50"
            >
              Annulla
            </button>
            <button
              type="button"
              onClick={handleRecover}
              disabled={recovering || !recoveryCode.trim()}
              className="flex-1 py-2.5 rounded-xl border-none font-bold text-xs text-white bg-ink disabled:opacity-60"
            >
              {recovering ? "Recupero…" : "Recupera"}
            </button>
          </div>
        </div>
      )}

      <div className="flex gap-1.5 mb-7">
        {[1, 2, 3].map((n) => (
          <div
            key={n}
            className={`h-[5px] flex-1 rounded-full ${step >= n ? "bg-office" : "bg-line"}`}
          />
        ))}
      </div>

      {step === 1 && (
        <StepCompany
          nickname={nickname}
          setNickname={setNickname}
          companyName={companyName}
          setCompanyName={setCompanyName}
          detected={detected}
          setDetected={setDetected}
          city={city}
          setCity={setCity}
          onNext={() => setStep(2)}
        />
      )}

      {step === 2 && (
        <StepPolicy
          companyName={companyName}
          policyType={policyType}
          setPolicyType={setPolicyType}
          policyPercent={policyPercent}
          setPolicyPercent={setPolicyPercent}
          policyDays={policyDays}
          setPolicyDays={setPolicyDays}
          onBack={() => setStep(1)}
          onNext={() => setStep(3)}
        />
      )}

      {step === 3 && (
        <StepSummary
          companyName={companyName}
          city={city}
          policyType={policyType}
          policyPercent={policyPercent}
          policyDays={policyDays}
          onBack={() => setStep(2)}
          onFinish={finishOnboarding}
          submitting={submitting}
          submitError={submitError}
        />
      )}
    </div>
  );
}

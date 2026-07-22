import { useState } from "react";
import { useSession } from "../../context/SessionContext.jsx";
import logo from "../../img/worklife-logo-header.png";
import StepCompany from "./StepCompany.jsx";
import StepPolicy from "./StepPolicy.jsx";
import StepSummary from "./StepSummary.jsx";

export default function OnboardingFlow() {
  const { completeOnboarding } = useSession();

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
      <div className="flex items-center mb-7">
        <img src={logo} alt="WorkLife Balance GM" className="h-8 w-auto" />
      </div>

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

import PhoneFrame from "./components/PhoneFrame.jsx";
import AppShell from "./components/app/AppShell.jsx";
import OnboardingFlow from "./components/onboarding/OnboardingFlow.jsx";
import { SessionProvider, useSession } from "./context/SessionContext.jsx";

function Screen() {
  const { status, error } = useSession();

  if (status === "loading") {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="w-8 h-8 rounded-full border-2 border-line border-t-ink animate-spin" />
      </div>
    );
  }

  return (
    <>
      {error && (
        <div className="absolute top-3 left-3 right-3 z-20 bg-pace-red-soft text-pace-red text-xs font-semibold rounded-xl px-3 py-2">
          {error}
        </div>
      )}
      {status === "onboarding" ? <OnboardingFlow /> : <AppShell />}
    </>
  );
}

export default function App() {
  return (
    <SessionProvider>
      <PhoneFrame>
        <Screen />
      </PhoneFrame>
    </SessionProvider>
  );
}

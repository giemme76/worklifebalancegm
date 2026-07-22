import AppShell from "./components/app/AppShell.jsx";
import Footer from "./components/Footer.jsx";
import OnboardingFlow from "./components/onboarding/OnboardingFlow.jsx";
import SessionCreated from "./components/onboarding/SessionCreated.jsx";
import PhoneFrame from "./components/PhoneFrame.jsx";
import { SessionProvider, useSession } from "./context/SessionContext.jsx";

function Screen() {
  const { status, error } = useSession();

  return (
    <div className="flex flex-col h-full">
      {error && (
        <div className="absolute top-3 left-3 right-3 z-20 bg-pace-red-soft text-pace-red text-xs font-semibold rounded-xl px-3 py-2">
          {error}
        </div>
      )}

      <div className="flex-1 min-h-0">
        {status === "loading" && (
          <div className="h-full flex items-center justify-center">
            <div className="w-8 h-8 rounded-full border-2 border-line border-t-ink animate-spin" />
          </div>
        )}
        {status === "onboarding" && <OnboardingFlow />}
        {status === "welcome" && <SessionCreated />}
        {status === "app" && <AppShell />}
      </div>

      <Footer />
    </div>
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

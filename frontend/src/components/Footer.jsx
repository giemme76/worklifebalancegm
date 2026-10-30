import { useState } from "react";
import HowItWorksModal from "./HowItWorksModal.jsx";

const GITHUB_REPO_URL = "https://github.com/giemme76/worklifebalancegm";

// Iniettato da vite.config.js al momento della build (git rev-parse HEAD).
const commit = typeof __GIT_COMMIT__ !== "undefined" ? __GIT_COMMIT__ : "unknown";
const commitShort = commit === "unknown" ? "unknown" : commit.slice(0, 7);
const commitUrl = commit === "unknown" ? GITHUB_REPO_URL : `${GITHUB_REPO_URL}/commit/${commit}`;

export default function Footer() {
  const [showHowItWorks, setShowHowItWorks] = useState(false);

  return (
    <>
      <div className="shrink-0 px-5 pt-2 pb-2.5 border-t border-line bg-surface flex flex-col gap-1">
        <button
          type="button"
          onClick={() => setShowHowItWorks(true)}
          className="self-center border-none bg-transparent p-0 text-[11px] font-bold text-office cursor-pointer"
        >
          Come funziona
        </button>
        <div className="flex items-center justify-between gap-3">
          <div className="text-[11px] text-muted">
            Realizzato da{" "}
            <a
              href="https://giemme76.com/"
              target="_blank"
              rel="noreferrer"
              className="font-bold text-office"
            >
              Giemme76
            </a>{" "}
            (
            <a
              href="https://www.linkedin.com/company/giemme76/"
              target="_blank"
              rel="noreferrer"
              className="font-bold text-office"
            >
              LinkedIn
            </a>
            )
          </div>
          <a
            href={commitUrl}
            target="_blank"
            rel="noreferrer"
            title="Ultimo commit su GitHub"
            className="text-[11px] font-bold text-office shrink-0 font-mono"
          >
            {commitShort}
          </a>
        </div>
      </div>
      {showHowItWorks && <HowItWorksModal onClose={() => setShowHowItWorks(false)} />}
    </>
  );
}

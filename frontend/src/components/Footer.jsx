const GITHUB_REPO_URL = "https://github.com/giemme76/worklifebalancegm";

// Iniettato da vite.config.js al momento della build (git rev-parse HEAD).
const commit = typeof __GIT_COMMIT__ !== "undefined" ? __GIT_COMMIT__ : "unknown";
const commitShort = commit === "unknown" ? "unknown" : commit.slice(0, 7);
const commitUrl = commit === "unknown" ? GITHUB_REPO_URL : `${GITHUB_REPO_URL}/commit/${commit}`;

export default function Footer() {
  return (
    <div className="shrink-0 px-5 py-2.5 border-t border-line bg-surface flex items-center justify-between gap-3">
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
  );
}

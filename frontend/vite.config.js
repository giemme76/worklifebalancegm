import { execSync } from "node:child_process";

import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// Commit corrente del repo al momento della build, mostrato nel footer con
// link alla pagina del commit su GitHub. "unknown" se il build gira fuori da
// un checkout git (non dovrebbe succedere nel flusso di deploy in uso).
function readGitCommit() {
  try {
    return execSync("git rev-parse HEAD").toString().trim();
  } catch {
    return "unknown";
  }
}

const gitCommit = readGitCommit();

// https://vitejs.dev/config/
export default defineConfig({
  // L'app viene pubblicata alla radice di smartworkingmanager.com.
  // Storicamente girava sotto https://giemme76.com/worklifebalancegm/ (path
  // dedicato, non radice): per rifare quel deploy, sovrascrivere con
  // VITE_BASE_PATH=/worklifebalancegm/ (vedi deploy.sh).
  base: process.env.VITE_BASE_PATH || "/",
  plugins: [react()],
  define: {
    __GIT_COMMIT__: JSON.stringify(gitCommit),
  },
  server: {
    port: 5173,
  },
});

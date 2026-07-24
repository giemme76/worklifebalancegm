import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// https://vitejs.dev/config/
export default defineConfig({
  // L'app viene pubblicata alla radice di smartworkingmanager.com.
  // Storicamente girava sotto https://giemme76.com/worklifebalancegm/ (path
  // dedicato, non radice): per rifare quel deploy, sovrascrivere con
  // VITE_BASE_PATH=/worklifebalancegm/ (vedi deploy.sh).
  base: process.env.VITE_BASE_PATH || "/",
  plugins: [react()],
  server: {
    port: 5173,
  },
});

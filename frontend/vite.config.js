import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// https://vitejs.dev/config/
export default defineConfig({
  // L'app viene pubblicata sotto https://giemme76.com/worklifebalancegm/,
  // non alla radice del dominio: senza questo, gli asset generati
  // punterebbero a /assets/... invece di /worklifebalancegm/assets/...
  // Sovrascrivibile in build con: vite build --base=/altro-path/
  base: process.env.VITE_BASE_PATH || "/worklifebalancegm/",
  plugins: [react()],
  server: {
    port: 5173,
  },
});

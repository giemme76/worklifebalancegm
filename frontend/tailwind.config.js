/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Manrope", "system-ui", "sans-serif"],
      },
      colors: {
        bg: "#fbfaf8",
        surface: "#ffffff",
        ink: "#26241f",
        muted: "oklch(0.55 0.012 70)",
        line: "oklch(0.9 0.008 70)",

        // Verde ripreso dal logo (WorkLifeBalanceGM-logo.png).
        office: { DEFAULT: "oklch(0.50 0.08 151)", soft: "oklch(0.94 0.03 151)" },
        smart: { DEFAULT: "oklch(0.6 0.09 210)", soft: "oklch(0.94 0.025 210)" },
        vacation: { DEFAULT: "oklch(0.72 0.1 85)", soft: "oklch(0.95 0.03 85)" },
        permit: { DEFAULT: "oklch(0.62 0.07 300)", soft: "oklch(0.94 0.02 300)" },
        sick: { DEFAULT: "oklch(0.65 0.1 340)", soft: "oklch(0.95 0.03 340)" },
        travel: { DEFAULT: "oklch(0.62 0.08 265)", soft: "oklch(0.94 0.02 265)" },

        pace: {
          green: "oklch(0.50 0.08 151)",
          "green-soft": "oklch(0.94 0.03 151)",
          orange: "oklch(0.68 0.14 55)",
          "orange-soft": "oklch(0.95 0.04 55)",
          red: "oklch(0.58 0.16 25)",
          "red-soft": "oklch(0.95 0.04 25)",
        },
      },
      borderRadius: {
        "4xl": "22px",
      },
      keyframes: {
        "wl-fade": { from: { opacity: 0 }, to: { opacity: 1 } },
        "wl-sheet-up": {
          from: { transform: "translateY(100%)" },
          to: { transform: "translateY(0)" },
        },
      },
      animation: {
        "wl-fade": "wl-fade .2s ease",
        "wl-sheet-up": "wl-sheet-up .22s cubic-bezier(.2,.8,.3,1)",
      },
    },
  },
  plugins: [],
};

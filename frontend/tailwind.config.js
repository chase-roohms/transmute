/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#ef4444',
          light: '#f87171',
          dark: '#dc2626',
        },
        accent: '#f59e0b',
        success: {
          DEFAULT: '#16a34a',
          light: '#22c55e',
          dark: '#15803d',
        },
        surface: {
          dark: '#0f172a',
          light: '#1e293b',
        },
        text: {
          DEFAULT: '#f8fafc',
          muted: '#94a3b8',
        },
      },
    },
  },
  plugins: [],
}

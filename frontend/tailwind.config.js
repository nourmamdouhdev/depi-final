/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        background: '#0a0a0a',
        surface: '#111111',
        border: '#27272a', // zinc-800
        muted: '#a1a1aa',  // zinc-400
        primary: '#ffffff',
        accent: '#3b82f6', // blue-500
      }
    },
  },
  plugins: [],
}

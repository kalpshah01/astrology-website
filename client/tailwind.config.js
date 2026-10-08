import typography from '@tailwindcss/typography';

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          dark: '#040b16', // Deep space blue/black
          light: '#fdf8f5', // Soft starlight white
          accent: '#fbbf24', // Amber/Gold for stars and highlights
          secondary: '#8b5cf6' // Mystic purple
        }
      }
    },
  },
  plugins: [
    typography,
  ],
}

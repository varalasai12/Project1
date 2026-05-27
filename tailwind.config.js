/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        glass: {
          light: 'rgba(255, 255, 255, 0.08)',
          dark: 'rgba(15, 23, 42, 0.3)',
          borderLight: 'rgba(255, 255, 255, 0.15)',
          borderDark: 'rgba(255, 255, 255, 0.05)',
        }
      },
      fontFamily: {
        sans: ['Outfit', 'Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse-slow 8s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin-slow': 'spin 12s linear infinite',
        'float': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        'pulse-slow': {
          '0%, 100%': { transform: 'scale(1) translate(0px, 0px)', opacity: 0.15 },
          '50%': { transform: 'scale(1.2) translate(15px, -15px)', opacity: 0.35 },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        }
      },
      backdropBlur: {
        xs: '2px',
      }
    },
  },
  plugins: [],
}

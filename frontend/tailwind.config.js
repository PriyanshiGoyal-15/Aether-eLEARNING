/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          dark: '#0B0F19',
          card: '#151D30',
          'card-hover': '#1F2942',
          light: '#F3F4F6',
          primary: '#6366F1',
          secondary: '#4F46E5',
          accent: '#10B981',
          danger: '#F43F5E',
          warning: '#F59E0B',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Outfit', 'sans-serif'],
      }
    },
  },
  plugins: [],
}

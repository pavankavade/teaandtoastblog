/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        toast: {
          50: '#fdfbf7',
          100: '#f7f2e9',
          200: '#ede1cd',
          300: '#dfcba8',
          400: '#cdac77',
          500: '#b88d4d',
          600: '#9b713c',
          700: '#7c5732',
          800: '#67472d',
          900: '#563c29',
          950: '#301f14',
        },
        tea: {
          50: '#fcf8f2',
          100: '#f7efe1',
          200: '#eeddc2',
          300: '#e1c49b',
          400: '#d2a472',
          500: '#c58853',
          600: '#b06f43',
          700: '#8e5436',
          800: '#744431',
          900: '#60392c',
          950: '#351b15',
        },
        warm: {
          light: '#FFFDF9',
          card: '#FFFFFF',
          border: '#F1ECE1',
          muted: '#78716C',
          dark: '#292524',
        }
      },
      fontFamily: {
        serif: ['"Playfair Display"', 'Georgia', 'serif'],
        sans: ['"Inter"', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      },
    },
  },
  plugins: [],
};

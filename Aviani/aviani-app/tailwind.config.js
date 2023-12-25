/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "one":"#88AB8E",
        "two":"#AFC8AD",
        "three":"#EEE7DA",
        "four":"#F2F1EB",
      }
    },
  },
  plugins: [],
}


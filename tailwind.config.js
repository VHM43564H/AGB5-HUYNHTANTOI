/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./*.html",
    "./**/*.html"
  ],
  safelist: [
    // Dynamic classes from JS in vi-mo.html (template literals)
    { pattern: /^(bg|text|border)-(emerald|rose|slate|orange|blue|purple|teal|amber|sky|green|red|yellow|indigo|violet|fuchsia|pink)-(50|100|200|300|400|500|600|700|800|900)$/ },
    { pattern: /^text-(emerald|rose|slate|orange|blue|purple|teal|amber)-(600|700|800)$/ },
    // Common ones used in cards etc.
    'col-span-full',
    'md:col-span-2',
    'lg:col-span-2',
  ],
  theme: {
    extend: {
      colors: {
        // Keep the primary gold used in the design
        primary: '#F5C400',
      }
    }
  },
  plugins: [],
}

module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Add any custom colors here
      },
      spacing: {
        // Add any custom spacing here
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
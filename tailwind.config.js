/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./wiki/**/*.html', './app.py'],
  theme: {
    extend: {
      fontFamily: {
        montserrat: ['Montserrat', 'sans-serif' ],
        lato: ['Lato', 'sans-serif']
      },
      colors: {
        "orange": "#ff9f00",
        "dark-blue": "#003153"
      },
      maxWidth: {
        "8xl": "88rem" 
      }
    },
  },
  plugins: [],
}


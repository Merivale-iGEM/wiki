/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./wiki/**/*.html", "./app.py"],
  theme: {
    extend: {
      fontFamily: {
        baron: ["Baron Neue", "sans-serif"],
        spartan: ["League Spartan", "sans-serif"],
      },
      colors: {
        primary: "#ff5757",
        bg: "#efefef",
        accent1: "#6d6d6d",
        accent2: "#242424",
      },
      maxWidth: {
        "8xl": "88rem",
      },
    },
  },
  plugins: [],
};

/** @type {import('tailwindcss').Config} */
module.exports = {
  purge: ['../templates/**/*.html'],
  content: [],
  theme: {
    extend: {
      colors:{
        'col-1': '#34495E',
        'col-2':'#20c997',
        'col-3':'#007bff'
      }
    },
  },
  plugins: [],
}


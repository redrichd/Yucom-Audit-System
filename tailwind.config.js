/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                'yucom-green': '#7FB069',
                'yucom-beige': '#F8F7F2',
                'yucom-red': '#E63946',
                'yucom-orange': '#F4A261',
            },
            fontFamily: {
                sans: ['"Noto Sans TC"', 'sans-serif'],
            }
        },
    },
    plugins: [],
}

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#101D2B",
        navy: "#192C3A",
        paper: "#F6F5F0",
        white: "#FFFFFF",
        sage: "#C7E8DC",
        "sage-dark": "#315C50",
        terracotta: "#D49B72",
        muted: "#77828A",
        border: "#E7E8E3",
        surface: "#EFEEE8",
      },
      fontFamily: {
        sans: ["var(--font-inter)", "sans-serif"],
        serif: ["var(--font-editorial)", "serif"],
      },
      spacing: {
        1: "0.25rem",
        2: "0.5rem",
        3: "0.75rem",
        4: "1rem",
        5: "1.25rem",
        6: "1.5rem",
        8: "2rem",
        10: "2.5rem",
        12: "3rem",
        16: "4rem",
        20: "5rem",
        24: "6rem",
      },
      maxWidth: {
        prose: "65ch",
        editorial: "720px",
        container: "1200px",
      },
    },
  },
  plugins: [],
};

import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        slatebg: '#050a14',
        panel: '#101a2d',
        borderc: '#223455',
        accent: '#42d3ff'
      }
    }
  },
  plugins: [],
};

export default config;

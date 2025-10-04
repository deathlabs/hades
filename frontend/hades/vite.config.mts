import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // Disable using URIs for data directives (e.g., img-src, font-src).
  build: {
    assetsInlineLimit: 0,
  }
});


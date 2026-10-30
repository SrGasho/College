import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

// La configuración de Vitest comparte el archivo de build.
// defineConfig aporta el tipado de la sección test.
export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: './src/test/setup.ts',
    css: true,
    exclude: ['backend/**', 'node_modules/**'],
  },
});

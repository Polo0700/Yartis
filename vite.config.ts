import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],

  // Tauri espera el dev server en este puerto
  server: {
    port: 3000,
    strictPort: true,
    watch: {
      ignored: (path) => {
        // Solo watchear src/ — ignorar todo lo demas
        return !path.includes('src');
      },
    },
  },
})

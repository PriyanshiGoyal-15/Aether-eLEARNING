import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  build: {
    chunkSizeWarningLimit: 1000, // Increase warning limit to 1000 kB (1MB)
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            if (id.includes('chart.js') || id.includes('vue-chartjs')) {
              return 'vendor-chartjs';
            }
            if (id.includes('lucide-vue-next')) {
              return 'vendor-icons';
            }
            return 'vendor-core';
          }
        }
      }
    }
  }
})

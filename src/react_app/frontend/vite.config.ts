import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const isDemoMode = mode === 'demo';
  
  return {
    plugins: [react()],
    // Use different entry points for demo vs production
    build: {
      rollupOptions: isDemoMode ? {
        input: './index-demo.html'
      } : {
        input: './index.html'
      }
    },
    server: {
      port: 5173,
      // Serve index-demo.html for demo mode
      ...(isDemoMode && {
        open: '/index-demo.html'
      }),
      // Only enable proxy for non-demo mode
      proxy: isDemoMode ? undefined : {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        },
        '/ws': {
          target: 'ws://localhost:8000',
          ws: true
        }
      }
    }
  };
})

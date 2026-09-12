import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [
    react(),
    {
      name: 'redirect-ip-to-localhost',
      configureServer(server) {
        server.middlewares.use((req, res, next) => {
          const host = req.headers.host || '';
          if (host.startsWith('localhost') || host.startsWith('127.0.0.1')) return next();
          const port = host.split(':')[1] || '3000';
          res.statusCode = 302;
          res.setHeader('Location', `http://localhost:${port}${req.url || '/'}`);
          res.end();
        });
      },
    },
  ],
  base: '/',
  server: {
    port: 3000,
    strictPort: false,
    host: true,
    open: true,
  },
});

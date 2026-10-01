import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// `npm run dev` on your Mac: /api is proxied to the backend on :8000,
// the same way nginx proxies it inside docker compose.
export default defineConfig({
  plugins: [react()],
  // antd is one big chunk; fine for an internal demo app, so silence the 500 kB warning.
  build: { chunkSizeWarningLimit: 1500 },
  server: {
    port: 5173,
    proxy: { "/api": "http://localhost:8000" },
  },
});

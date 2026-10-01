import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// `npm run dev` on your Mac: /api is proxied to the backend on :8000,
// the same way nginx proxies it inside docker compose.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: { "/api": "http://localhost:8000" },
  },
});

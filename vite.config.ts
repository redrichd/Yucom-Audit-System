import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/Yucom-Audit-System/', // 必須與 GitHub 儲存庫名稱一致
})
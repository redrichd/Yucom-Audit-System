# 任務清單 (Tasks)

**專案**: 悠康電子服務紀錄稽核系統 (Yucom Audit System)
**文件狀態**: 待執行

## 第一階段: 專案設定 (Setup)
- [ ] T001 建立專案目錄結構與 .gitignore 設定 (前端/後端分離) `project_root/`
- [ ] T002 安裝前端依賴 (React 18, Vite, Tailwind, react-pdf-viewer) `package.json`
- [ ] T003 設定 Tailwind CSS 品牌色票與 Noto Sans TC 字體 `tailwind.config.js`
- [ ] T004 建立 FastAPI 後端基礎架構與虛擬環境 `backend/main.py`
- [ ] T005 [P] 設定 ESLint, Prettier 與 Python Black formatter `.eslintrc`, `pyproject.toml`

## 第二階段: 基礎建設 (Foundational)
- [ ] T006 [P] 實作前端 Main Layout (75%/25% 雙欄響應式佈局) `src/layouts/MainLayout.tsx`
- [ ] T007 [P] 實作後端 API 基礎路由與 CORS 設定 `backend/api/routes.py`
- [ ] T008 [P] 建立共用型別定義 (AuditResult, ServiceRecord) `src/types/index.ts`
- [ ] T009 實作 PDF 檔案上傳元件 (Drag & Drop) `src/components/PdfUploader.tsx`

## 第三階段: [US2] PDF 上傳與預覽
- [ ] T010 [US2] 整合 react-pdf-viewer 核心渲染元件 `src/components/PdfViewer.tsx`
- [ ] T011 [US2] 實作 `URL.createObjectURL` 與記憶體清理機制 `src/hooks/usePdfLoader.ts`
- [ ] T012 [US2] 串接後端 `/api/upload` (Memory-only bytes handling) `backend/api/endpoints/upload.py`

## 第四階段: [US3] 自動化稽核分析
- [x] T013 [P] [US3] 實作 pdfplumber 文字座標解析服務 `backend/services/pdf_parser.py` (Added: Rects/Curves/Images support)
- [x] T014 [US3] 實作 YC01-8 (時數重疊) 邏輯檢核函式 `backend/logic/yc01_rules.py`
- [x] T015 [US3] 實作 YC02-3 (簽名欄偵測) 邏輯 - 支援手寫筆跡 (Curves/Images) 與文字 `backend/logic/yc02_rules.py`
- [ ] T024 [US3] 實作 YC03-1 (BA16-1 代購備註) 邏輯 - 檢查代購品項與金額 `backend/logic/yc03_rules.py`
- [ ] T025 [US3] 實作 YC04-1 (BA05-1 備餐菜色) 邏輯 - 檢查備餐細節 (粥, 飯, 菜, 水...) `backend/logic/yc04_rules.py`
- [ ] T026 [US3] 實作 YC01 系列靜態檢查 (YC01-5 BodyStatus, YC01-6 Summary, YC01-7 Temp, YC01-8 Fields) `backend/logic/static_checks.py`
- [ ] T027 [US3] 實作 YC04 系列時間邏輯 (YC02-5 TimeCalc, YC04-7 Overtime) `backend/logic/time_checks.py`
- [ ] T028 [US3] 實作 YC01-10 備註檢查整合 (BA13/14/16/05) `backend/logic/content_checks.py`
- [x] T029 [US3] 實作跨頁判定邏輯 (group_pages_by_case) `backend/services/pdf_parser.py`
- [x] T030 [US3] 重構規則模組以支援 RecordGroup 上下文 (YC02, Static Checks)
- [x] T031 [US3] 實作未執行紀錄略過邏輯 (is_record_active) `backend/logic/pre_check.py`
- [ ] T016 [US3] 定義標準化 API 回傳格式 (含座標資訊) `backend/schemas/audit.py`

## 第五階段: [US4] 異常標註與結果呈現
- [ ] T017 [US4] 實作右側稽核結果列表元件 `src/components/AuditSidebar.tsx`
- [ ] T018 [US4] 實作 Canvas Overlay 層以繪製異常紅框 `src/components/CanvasOverlay.tsx`
- [ ] T019 [US4] 實作點擊列表項目自動捲動至 PDF 對應頁面功能 `src/hooks/usePdfNavigation.ts`
- [ ] T020 [US4] 整合前端狀態管理 (Zustand/Context) 同步顯示 `src/store/auditStore.ts`

## 最終階段: 優化與安全性 (Polish)
- [ ] T021 執行全系統效能測試 (50頁 PDF < 5s) `tests/performance_test.py`
- [ ] T022 驗證記憶體洩漏 (Memory Leak Check) `docs/security_audit.md`
- [ ] T023 撰寫使用者操作手冊 (zh-TW) `docs/manual.md`

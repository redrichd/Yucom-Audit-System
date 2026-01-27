# 實作計畫書 (Implementation Plan)

**專案名稱**: 悠康電子服務紀錄稽核系統 (Yucom Audit System)
**版本**: 1.0.0
**日期**: 2026-01-27

## 技術背景 (Technical Context)

本計畫書旨在定義「悠康電子服務紀錄稽核系統」的技術實作細節。系統將採用現代化的前後端分離架構，專注於高效能的 PDF 處理與嚴謹的醫療資料稽核。

### 技術堆疊 (Tech Stack)

*   **前端**: React 18, TypeScript, Vite, Tailwind CSS
*   **後端**: Python 3.10+, FastAPI (Localhost only)
*   **PDF 引擎**: `pdf.js` (渲染), `pdfplumber` (座標與物件提取：Text, Curves, Images)
*   **通訊協定**: RESTful API (HTTP/JSON)
*   **資料流**: Memory-Only (檔案上傳後僅存在於 RAM，分析完畢即釋放)

## 憲章核對 (Constitution Check)

本計畫已核對以下核心原則：
- [x] **資料隱私**: 遵守 Memory-Only 原則，不上傳雲端，不寫入硬碟。
- [x] **UI/UX 標準**: 使用 75%/25% 雙欄布局與品牌色。
- [x] **語言規範**: 所有產出物使用繁體中文 (zh-TW)。
- [x] **邏輯精確性**: 整合 YC01~YC08 標準稽核邏輯。

## 階段規劃 (Phases)

### 第一階段：專案初始化與基礎建設 (Setup & Foundation)
- 建置 Vite + React 專案結構。
- 設定 Tailwind CSS 與 Yucom 品牌色票。
- 整合 React PDF Viewer。
- 設定 Python FastAPI 基礎環境。

### 第二階段：核心功能實作 (Core Implementation)
- **PDF 上傳與預覽**: 實作檔案拖曳上傳與 75% 寬度預覽區。
- **後端解析 API**: 實作 `/api/audit` 端點，接收 PDF 並回傳座標與異常。
- **稽核側邊欄 (Sidebar)**: 實作 25% 寬度的結果顯示區。

### 第三階段：邏輯整合與優化 (Logic & Polish)
- **Static Checks**: YC01 (欄位/簽名/體溫/概況), YC05 (身心狀況)。
- **Logic Checks**: YC01-10 (備註: BA16/BA05/BA13...), YC02-5 (時間計算), YC04-7 (超時)。
- **座標映射 (Mapping)**: 將後端回傳的 `(x, y, w, h)` 繪製於前端 Canvas 層。
- **記憶體優化**: 確保 `URL.revokeObjectURL()` 在適當時機觸發。

## 風險評估 (Risk Assessment)

- **座標偏移**: 不同解析度的 PDF 可能導致標註框位移。需實作響應式座標轉換。
- **大檔案效能**: 超過 50頁的 PDF 可能導致瀏覽器卡頓。需採用虛擬列表 (Virtualization)。

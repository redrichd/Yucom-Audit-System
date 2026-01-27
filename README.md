# 悠康電子服務紀錄稽核系統 (Yucom Audit System)

![Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 專案簡介 (Project Overview)

悠康電子服務紀錄稽核系統是一個專為居家照護服務設計的自動化稽核工具。本系統旨在協助機構快速檢核 PDF 格式的服務紀錄單，確保數據準確性、合規性，並提升行政效率。

### 核心功能 (Core Features)

*   **PDF 自動解析**: 使用 `pdf.js` 與 `pdfplumber` 精確提取服務紀錄內容。
*   **視覺化稽核**: 左右並排的 75%/25% 分割介面，左側顯示原始 PDF，右側顯示稽核結果與異常標記。
*   **YC 邏輯自動檢核 (YC Rules)**: 內建 YC01 至 YC08 等標準稽核邏輯，自動計算時數與核對醫囑。
*   **隱私保護**: 資料處理全程採用 Memory-Only 機制，不將敏感個資寫入硬碟。

## 技術架構 (Technology Stack)

本專案嚴格遵循最新的 Yucom 技術規範：

*   **Frontend**: React 18 (TypeScript), Vite, Tailwind CSS
*   **PDF Engine**: `@react-pdf-viewer/core`, `pdfjs-dist`
*   **Backend**: Python 3.10+, FastAPI (Localhost API)
*   **Design**: Noto Sans TC (字體), Yucom Brand Colors (草本綠 #7FB069)

## 快速開始 (Quick Start)

### 前置需求 (Prerequisites)

*   Node.js v20+
*   Python 3.10+

### 安裝步驟 (Installation)

1.  **複製專案 (Clone)**:
    ```bash
    git clone https://github.com/your-org/yucom-audit.git
    cd yucom-audit
    ```

2.  **安裝前端依賴 (Frontend)**:
    ```bash
    npm install
    ```

3.  **啟動開發伺服器 (Dev Server)**:
    ```bash
    npm run dev
    ```

4.  **建置專案 (Build)**:
    ```bash
    npm run build
    ```

## 專案結構 (Directory Structure)

```
/
├── public/              # 靜態資源
├── src/
│   ├── components/      # UI 元件 (基於 Tailwind)
│   ├── App.tsx          # 主應用程式入口
│   ├── main.tsx         # React 渲染點
│   └── index.css        # Tailwind 樣式設定
├── .github/workflows/   # CI/CD 自動化流程
├── package.json         # 前端依賴設定
├── vite.config.ts       # Vite 設定檔
└── README.md            # 專案說明文件
```

## 開發規範 (Guidelines)

*   **語言**: 所有文檔、註解、Commit Message 必須使用**繁體中文 (zh-TW)**。
*   **代碼風格**: 前端遵循 ESLint + Prettier 規則。
*   **資安**: 嚴禁將任何測試用的 PDF 個資上傳至 Git 倉庫。

## 部署 (Deployment)

本專案配置了 GitHub Actions (`.github/workflows/deploy.yml`)，每次推送至 `main` 分支時會自動觸發：
1. 安裝依賴
2. 執行 ESLint 檢查
3. 執行 Build 建置
4. 生成 `dist/` 部署包

## 授權 (License)

MIT License

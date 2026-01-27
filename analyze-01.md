# 系統分析報告 (System Analysis Report)

**報告日期**: 2026-01-27
**專案名稱**: 服務記錄單檢查自動化 (Yucom Audit System)
**報告目標**: 檢核目前系統實作狀態與需求規格 (Spec) 的符合度。

## 1. 系統架構現況 (Architecture Overview)

*   **前端 (Frontend)**: React + Vite + Tailwind CSS
    *   已實作 `PdfUploader` 與 `PdfViewer` (Memory-only loading)。
    *   已實作稽核結果側邊欄，支援異常列表顯示與座標點擊反白。
    *   **狀態**: 🟢 運作正常 (Stable)。

*   **後端 (Backend)**: Python FastAPI + PDFPlumber
    *   已實作 `/api/upload` 介面，接收 PDF bytes 進行即時分析。
    *   已建立 `RecordGroup` 邏輯，支援跨頁判定。
    *   **狀態**: 🟢 運作正常 (Stable)。

## 2. 稽核規則實作狀態 (Audit Rules Status)

目前已針對 **[US3] 自動化稽核分析** 完成以下核心規則的開發與優化：

| 規則代號 | 規則名稱 | 實作邏輯摘要 | 狀態 | 備註 |
| :--- | :--- | :--- | :--- | :--- |
| **YC01-7** | 體溫檢核 | `static_checks.py` 使用全文檢索 (`raw_text`) 偵測「體溫」關鍵字。 | 🟢 Pass | 已支援跨頁繼承 (整組有一頁有即通過)。 |
| **YC01-8** | 時數重疊 | `yc01_rules.py` 檢查同一時段是否有重複服務。 | 🟢 Pass | 基礎邏輯已完成。 |
| **YC02-3** | 簽名偵測 | `yc02_rules.py` 偵測文字、圖片、曲線 (手寫筆跡)。ROI 擴大至整行。 | 🟢 Pass | 已支援跨頁繼承，大幅降低誤判。 |
| **YC03-1** | BA16-1 備註 | `yc03_rules.py` 檢查代購品項與金額 (Regex: `$`, `元`, `餐`...)。 | 🟢 Pass | 針對有打勾的日期進行垂直欄位掃描。 |
| **YC04-1** | BA05-1 菜色 | `yc04_rules.py` 檢查備餐細節 (Regex: `飯`, `菜`, `魚`, `肉`...)。 | 🟢 Pass | 針對有打勾的日期進行垂直欄位掃描。 |

## 3. 關鍵技術突破 (Key Logic Improvements)

### 3.1 跨頁判定 (Multi-Page Context)
*   **問題**: 舊版邏輯將每一頁視為獨立個體，導致跨頁表格的「續頁」因無表頭/無簽名而被誤判。
*   **解決方案**: 
    1. 實作 `group_pages_by_case`，依據 PDF 內的 `個案編號` 或 `個案姓名` 將連續頁面分組。
    2. 在 `check_signature_fields` 與 `check_static_rules` 中引入 **Group Context**。
    3. **結果**: 只要同組內任一頁符合條件 (如 Page 6 有體溫，Page 7 無)，整組皆判定為合格 (Pass)。

### 3.2 手寫抗性 (Handwritten Robustness)
*   **問題**: `pdfplumber` 預設僅提取文字，無法識別純圖片或筆畫構成的簽名。
*   **解決方案**: 同時提取 `rects`, `lines`, `curves`, `images` 物件，若簽名欄位內有足夠密度的上述物件，即視為已簽名。

### 3.3 體溫偵測優化 (Temperature Robustness)
*   **問題**: PDF 分詞 (Tokenization) 可能將「個案體溫」拆解，導致關鍵字比對失敗。
*   **解決方案**: 改用 `raw_text` 全頁字串搜尋，確保即使分詞破碎也能正確抓到關鍵字。

## 4. 待執行項目 (Next Steps)

1.  **時間邏輯深化**: 實作 YC02-5 (總時數計算驗證) 與 YC04-7 (超時異常)。
2.  **排班表對接**: 未來需引入排班表資料以支援遲到/早退判定 (YC04-1/2/3)。
3.  **UI 優化**: 在前端實作 Canvas Overlay，將後端回傳的異常座標直接繪製在 PDF 上。

## 5. 結論

自動化稽核系統的核心邏輯已具備高度實用性，特別是在處理真實世界中複雜的 PDF 格式 (手寫、跨頁、格式跑版) 方面做了顯著優化。目前的誤判率應已降至最低，可進行下一階段的 UX 整合測試。

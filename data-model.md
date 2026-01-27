# 資料模型 (Data Model)

## 核心實體 (Core Entities)

### 1. 服務紀錄單 (ServiceRecord)
代表一份上傳的 PDF 文件。

| 欄位 | 類型 | 說明 |
| --- | --- | --- |
| `file_name` | string | 原始檔名 |
| `total_pages` | int | 總頁數 |
| `service_date` | date | 服務月份/日期 |
| `caregiver_id` | string | 照服員編號 |
| `client_id` | string | 個案編號 |

### 2. 稽核項目 (AuditItem)
系統針對單一紀錄單檢查出的具體項目。

| 欄位 | 類型 | 說明 |
| --- | --- | --- |
| `id` | uuid | 唯一識別碼 |
| `rule_id` | string | 對應的 YC 規則 (如 "YC01-8") |
| `status` | enum | `PASS` (通過) / `FAIL` (異常) / `WARN` (警示) |
| `message` | string | 異常說明訊息 |
| `coordinates` | object | `{ page: 1, x: 100, y: 200, w: 50, h: 20 }` (PDF 座標) |

## YC 邏輯規則庫 (YC Rules)

| 規則 ID | 名稱 | 邏輯描述 |
| --- | --- | --- |
| **YC01-8** | 總時數檢核 | 每日服務總時數不得超過 12 小時，且單次服務區間不得重疊。 |
| **YC02-3** | 簽名檢核 | 服務紀錄單必須有照服員與個案/家屬簽名 (偵測簽名欄位是否為空)。 |
| **YC05-1** | 醫囑比對 | 服務項目代碼必須與當月醫囑單相符。 |

## API 介面 (API Draft)

### `POST /api/audit/analyze`
接收 PDF 檔案，回傳稽核結果。

**Request**:
- `file`: Multipart Form Data (PDF binary)

**Response**:
```json
{
  "record_meta": {
    "file_name": "2023-10_L12345.pdf",
    "total_pages": 3
  },
  "audit_results": [
    {
      "id": "uuid-...",
      "rule_id": "YC01-8",
      "status": "FAIL",
      "message": "服務時間重疊：10:00-11:00 與 10:30-11:30",
      "coordinates": { "page": 1, "x": 50, "y": 500, "w": 200, "h": 20 }
    }
  ]
}
```

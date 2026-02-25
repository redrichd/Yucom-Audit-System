import React, { useState } from 'react'; // 修正：現在 React 會被用到
import { auditApi } from './api/auditApi';

function App() {
    const [auditResults, setAuditResults] = useState<any[]>([]);
    const [isAnalyzing, setIsAnalyzing] = useState(false);

    // 修正：這個 handleUpload 現在會被按鈕觸發
    const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        setIsAnalyzing(true);
        setAuditResults([]);

        try {
            const response = await auditApi.upload(file);
            // 關鍵修正：對接後端包裹格式，解決 reading 'length' 錯誤
            setAuditResults(response.data.results || []);
        } catch (error) {
            alert("分析失敗，請確認後端已起床 (初次啟動需 50 秒)");
        } finally {
            setIsAnalyzing(false);
        }
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>悠康電子服務紀錄稽核系統</h1>

            {/* 修正：在這裡綁定功能，消滅 unused 警告 */}
            <input type="file" accept=".pdf" onChange={handleUpload} disabled={isAnalyzing} />

            {isAnalyzing && <p>AI 正在稽核中，269 頁可能需要 1-3 分鐘...</p>}

            <div style={{ marginTop: '20px' }}>
                <h3>稽核結果 (共 {auditResults?.length || 0} 項)</h3>
                {auditResults.map((res, i) => (
                    <div key={i} style={{ borderBottom: '1px solid #ccc', padding: '10px 0' }}>
                        <strong>第 {res.page} 頁</strong>: {res.message}
                    </div>
                ))}
            </div>
        </div>
    );
}

export default App; // 修正：確保 App 被匯出
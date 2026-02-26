import React, { useState } from 'react';
import { auditApi } from './api/auditApi';

function App() {
    // 初始化為空陣列，徹底防禦 reading 'length' 的崩潰
    const [auditResults, setAuditResults] = useState<any[]>([]);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [pdfUrl, setPdfUrl] = useState<string | null>(null);

    const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        // 建立預覽網址
        const url = URL.createObjectURL(file);
        setPdfUrl(url);

        // 開始分析
        setIsAnalyzing(true);
        setAuditResults([]); // 清空舊結果

        try {
            const response = await auditApi.upload(file);
            // 關鍵修正：從 response.data.results 提取資料
            setAuditResults(response.data.results || []);
        } catch (error) {
            alert("分析失敗，請檢查 Render 伺服器狀態");
        } finally {
            setIsAnalyzing(false);
        }
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', fontFamily: 'sans-serif' }}>
            <header style={{ padding: '10px 20px', background: '#f5f5f5', borderBottom: '1px solid #ddd' }}>
                <h2 style={{ color: '#2c5282', margin: 0 }}>悠康電子服務紀錄稽核系統</h2>
            </header>

            <main style={{ display: 'flex', flex: 1, overflow: 'hidden' }}>
                {/* 左側：PDF 預覽區 */}
                <div style={{ flex: 1, borderRight: '1px solid #ddd', background: '#525659' }}>
                    {pdfUrl ? (
                        <iframe src={pdfUrl} width="100%" height="100%" title="PDF Preview" />
                    ) : (
                        <div style={{ color: 'white', display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                            請選擇 PDF 檔案以開啟預覽
                        </div>
                    )}
                </div>

                {/* 右側：狀態與結果區 */}
                <div style={{ width: '350px', padding: '20px', overflowY: 'auto', background: 'white' }}>
                    <div style={{ marginBottom: '20px' }}>
                        <input type="file" accept=".pdf" onChange={handleFileChange} disabled={isAnalyzing} />
                    </div>

                    <div style={{ padding: '15px', borderRadius: '8px', background: isAnalyzing ? '#ebf8ff' : '#f0fff4', marginBottom: '20px' }}>
                        <h4 style={{ margin: '0 0 5px 0' }}>稽核狀態</h4>
                        <p style={{ margin: 0, color: isAnalyzing ? '#3182ce' : '#38a169' }}>
                            {isAnalyzing ? "正在分析中... (Analyzing)" : "尚未開始分析或已完成"}
                        </p>
                    </div>

                    <div>
                        <h4 style={{ borderBottom: '2px solid #eee', paddingBottom: '10px' }}>
                            檢核結果 ({auditResults?.length || 0} 項)
                        </h4>
                        {auditResults.length > 0 ? (
                            auditResults.map((res, i) => (
                                <div key={i} style={{ padding: '10px', borderBottom: '1px solid #f0f0f0', fontSize: '14px' }}>
                                    <span style={{ fontWeight: 'bold', color: '#e53e3e' }}>第 {res.page} 頁</span>: {res.message}
                                </div>
                            ))
                        ) : (
                            <p style={{ color: '#a0aec0' }}>尚無異常或未開始分析</p>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
}

export default App;
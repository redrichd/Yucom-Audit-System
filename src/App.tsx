import React, { useState } from 'react';
import { auditApi } from './api/auditApi';

function App() {
    // 初始化為空陣列，防止讀取 .length 時崩潰
    const [auditResults, setAuditResults] = useState<any[]>([]);
    const [isAnalyzing, setIsAnalyzing] = useState(false);

    const handleUpload = async (file: File) => {
        setIsAnalyzing(true);
        try {
            const response = await auditApi.upload(file);
            // 修正點：從 results 屬性中提取資料
            setAuditResults(response.data.results || []);
        } catch (error) {
            alert("分析失敗，請檢查網路連線");
        } finally {
            setIsAnalyzing(false);
        }
    };

    return (
        <div className="App">
            {/* 渲染 UI ... */}
            <p>稽核狀態: {isAnalyzing ? "正在分析中..." : "分析完成"}</p>

            {/* 使用 ?. 安全讀取，防止畫面全白 */}
            <p>共發現 {auditResults?.length || 0} 個項目</p>

            {auditResults.map((res, idx) => (
                <div key={idx}>第 {res.page} 頁: {res.message}</div>
            ))}
        </div>
    );
}
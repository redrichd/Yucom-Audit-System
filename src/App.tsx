
import { useState } from 'react'
import { MainLayout } from './layouts/MainLayout'
import { PdfUploader } from './components/PdfUploader'
import { PdfViewer } from './components/PdfViewer' // Import Viewer
import { usePdfLoader } from './hooks/usePdfLoader' // Import Hook
import { auditApi } from './api/auditApi'
import { AuditResult } from './types'

function App() {
    const [currentFile, setCurrentFile] = useState<File | null>(null);
    const [auditResults, setAuditResults] = useState<AuditResult[]>([]);
    const [isAnalyzing, setIsAnalyzing] = useState(false);

    // Use the hook to get the blob URL
    const { pdfUrl, error } = usePdfLoader(currentFile);

    const handleFileSelect = async (file: File) => {
        console.log("File selected:", file.name);
        setCurrentFile(file);
        setAuditResults([]); // Reset results

        // Upload to backend
        setIsAnalyzing(true);
        try {
            const response = await auditApi.uploadFile(file);
            setAuditResults(response.audit_results);
            console.log("Audit complete:", response.audit_results);
        } catch (err) {
            console.error("Analysis failed", err);
            alert("分析失敗，請確認後端伺服器已啟動 (localhost:8000)");
        } finally {
            setIsAnalyzing(false);
        }
    };

    const LeftPanel = (
        <div className="flex h-full w-full flex-col items-center justify-center">
            {!currentFile ? (
                <PdfUploader onFileSelect={handleFileSelect} />
            ) : (
                <div className="flex h-full w-full flex-col">
                    <div className="flex items-center justify-between border-b bg-white px-4 py-2 shadow-sm">
                        <span className="font-medium text-gray-700">預覽: {currentFile.name}</span>
                        <button
                            onClick={() => {
                                setCurrentFile(null);
                                setAuditResults([]);
                            }}
                            className="text-sm text-red-500 hover:text-red-700"
                        >
                            關閉檔案
                        </button>
                    </div>

                    <div className="flex-1 overflow-hidden bg-gray-100">
                        {error ? (
                            <div className="flex h-full items-center justify-center text-red-500">
                                {error}
                            </div>
                        ) : pdfUrl ? (
                            <PdfViewer fileUrl={pdfUrl} />
                        ) : (
                            <div className="flex h-full items-center justify-center text-gray-400">
                                載入中...
                            </div>
                        )}
                    </div>
                </div>
            )}
        </div>
    );

    const RightPanel = (
        <div className="space-y-4">
            <div className="rounded-lg bg-green-50 p-4 text-yucom-green">
                <h3 className="font-bold border-b border-green-200 pb-2 mb-2">稽核狀態</h3>
                {!currentFile ? (
                    <p>等待檔案上傳...</p>
                ) : isAnalyzing ? (
                    <p className="animate-pulse">正在分析中... (Analyzing)</p>
                ) : (
                    <p>分析完成。共發現 {auditResults.length} 個項目。</p>
                )}
            </div>

            <div className="rounded-lg border border-gray-200 bg-white p-4">
                <h3 className="font-bold text-gray-700 mb-2">檢核結果 (Results)</h3>
                {auditResults.length === 0 ? (
                    <ul className="space-y-2 text-sm text-gray-500">
                        <li className="flex items-center text-gray-400 italic">
                            尚無異常或未開始分析
                        </li>
                    </ul>
                ) : (
                    <ul className="space-y-3">
                        {auditResults.map((res) => (
                            <li key={res.id} className="rounded border-l-4 border-red-500 bg-red-50 p-2 text-sm shadow-sm cursor-pointer hover:bg-red-100">
                                <div className="font-bold text-red-700">{res.rule_id} {res.status}</div>
                                <div className="text-gray-700">{res.message}</div>
                                <div className="text-xs text-gray-400 mt-1">Page {res.coordinates.page}</div>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );

    return (
        <MainLayout
            leftPanel={LeftPanel}
            rightPanel={RightPanel}
        />
    )
}

export default App

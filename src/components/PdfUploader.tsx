import React, { useCallback } from 'react';

interface PdfUploaderProps {
    onFileSelect: (file: File) => void;
}

export const PdfUploader: React.FC<PdfUploaderProps> = ({ onFileSelect }) => {
    const handleDrop = useCallback(
        (e: React.DragEvent<HTMLDivElement>) => {
            e.preventDefault();
            e.stopPropagation();

            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                const file = e.dataTransfer.files[0];
                if (file.type === "application/pdf") {
                    onFileSelect(file);
                } else {
                    alert("請上傳 PDF 格式檔案");
                }
            }
        },
        [onFileSelect]
    );

    const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            onFileSelect(e.target.files[0]);
        }
    };

    return (
        <div
            className="flex h-full w-full flex-col items-center justify-center rounded-lg border-2 border-dashed border-yucom-green bg-white p-12 text-center transition-colors hover:bg-green-50"
            onDrop={handleDrop}
            onDragOver={handleDragOver}
        >
            <div className="mb-4 rounded-full bg-green-100 p-4">
                <svg className="h-10 w-10 text-yucom-green" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
            </div>
            <h3 className="mb-2 text-xl font-bold text-gray-700">上傳服務紀錄單</h3>
            <p className="mb-6 text-gray-500">將 PDF 檔案拖曳至此，或點擊下方按鈕選擇檔案</p>

            <label className="cursor-pointer rounded-md bg-yucom-green px-6 py-2 text-white transition-colors hover:bg-green-700">
                選擇檔案
                <input
                    type="file"
                    className="hidden"
                    accept="application/pdf"
                    onChange={handleFileInput}
                />
            </label>
            <p className="mt-4 text-xs text-gray-400">支援最大 50MB PDF 檔案</p>
        </div>
    );
};

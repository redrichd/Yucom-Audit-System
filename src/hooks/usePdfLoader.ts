import { useState, useEffect } from 'react';

interface UsePdfLoaderResult {
    pdfUrl: string | null;
    error: string | null;
}

export const usePdfLoader = (file: File | null): UsePdfLoaderResult => {
    const [pdfUrl, setPdfUrl] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!file) {
            setPdfUrl(null);
            return;
        }

        try {
            // Create a Blob URL for the PDF file (Memory-only)
            const objectUrl = URL.createObjectURL(file);
            setPdfUrl(objectUrl);

            // Cleanup function to revoke the URL when the component unmounts or file changes
            return () => {
                if (objectUrl) {
                    URL.revokeObjectURL(objectUrl);
                    console.log("PDF Object URL revoked:", objectUrl);
                }
            };
        } catch (err) {
            console.error("Error creating object URL:", err);
            setError("無法讀取 PDF 檔案");
            setPdfUrl(null);
        }
    }, [file]);

    return { pdfUrl, error };
};

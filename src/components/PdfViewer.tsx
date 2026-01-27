import React from 'react';
import { Viewer, Worker } from '@react-pdf-viewer/core';
import { defaultLayoutPlugin } from '@react-pdf-viewer/default-layout';

// Import styles
import '@react-pdf-viewer/core/lib/styles/index.css';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';

// Worker should be hosted locally or via CDN matching the version.
// Using pdfjs-dist version matching package.json (3.11.174)
// Vite usually handles this, but explicit worker URL is safer.
import pdfWorker from 'pdfjs-dist/build/pdf.worker.min.js?url';

interface PdfViewerProps {
    fileUrl: string;
}

export const PdfViewer: React.FC<PdfViewerProps> = ({ fileUrl }) => {
    const defaultLayoutPluginInstance = defaultLayoutPlugin();

    return (
        <div className="h-full w-full">
            <Worker workerUrl={pdfWorker}>
                <div style={{ height: '100%', width: '100%' }}>
                    <Viewer
                        fileUrl={fileUrl}
                        plugins={[
                            defaultLayoutPluginInstance,
                        ]}
                        theme={{
                            theme: 'auto',
                        }}
                        localization={{
                            // Simple localization if needed, or default English
                        }}
                    />
                </div>
            </Worker>
        </div>
    );
};

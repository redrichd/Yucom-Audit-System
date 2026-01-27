import React, { ReactNode } from 'react';

interface MainLayoutProps {
    leftPanel: ReactNode;
    rightPanel: ReactNode;
}

export const MainLayout: React.FC<MainLayoutProps> = ({ leftPanel, rightPanel }) => {
    return (
        <div className="flex h-screen w-full flex-col bg-yucom-beige">
            {/* Header */}
            <header className="flex h-16 items-center border-b border-gray-200 bg-white px-6 shadow-sm">
                <h1 className="text-xl font-bold text-yucom-green">
                    悠康電子服務紀錄稽核系統
                </h1>
                <div className="ml-auto text-sm text-gray-500">
                    系統版本: v0.1.0
                </div>
            </header>

            {/* Main Content Area (Fixed 75% / 25% Split) */}
            <main className="flex flex-1 overflow-hidden">
                {/* Left Panel: 75% Width - PDF Viewer */}
                <div className="h-full w-3/4 border-r border-gray-200 bg-gray-50 p-4 overflow-auto">
                    {leftPanel}
                </div>

                {/* Right Panel: 25% Width - Audit Sidebar */}
                <div className="h-full w-1/4 bg-white p-4 overflow-auto shadow-inner">
                    {rightPanel}
                </div>
            </main>
        </div>
    );
};

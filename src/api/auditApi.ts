import { AuditResponse } from '../types';

const API_BASE_URL = 'https://yucom-audit-backend.onrender.com/api';

export const auditApi = {
    async uploadFile(file: File): Promise<AuditResponse> {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${API_BASE_URL}/upload`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    async checkHealth(): Promise<boolean> {
        try {
            const res = await fetch(`${API_BASE_URL.replace('/api', '')}/health`);
            return res.ok;
        } catch {
            return false;
        }
    }
};

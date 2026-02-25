import axios from 'axios';

const api = axios.create({
    baseURL: 'https://yucom-audit-backend.onrender.com/api', // 您的 Render 網址
});

export const auditApi = {
    upload: (file: File) => {
        const formData = new FormData();
        formData.append('file', file);
        return api.post('/upload', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
    },
};
import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
});

api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export const loginUser = async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await api.post('/auth/login', formData);
    return response.data;
};

export const signupUser = async (email, password) => {
    const response = await api.post('/auth/signup', { email, password });
    return response.data;
};

export const askQuestion = async (query) => {
    const response = await api.post('/chat/ask', { query, role: 'user' });
    return response.data;
};

export default api;

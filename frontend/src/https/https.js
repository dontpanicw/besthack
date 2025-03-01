import axios from "axios";

// Используем переменные окружения или резервные значения
export const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const api = axios.create({
    withCredentials: true,
    baseURL: API_URL
})

api.interceptors.request.use((config) => {
    config.headers.Authorization = `Bearer ${localStorage.getItem('token')}`

    return config;
})


export default api;
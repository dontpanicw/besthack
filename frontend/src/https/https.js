import axios from "axios";
import { handleUnauthorized } from "../AuthManager";


export const API_URL = "http://31.130.150.30:8000";

const api = axios.create({
    withCredentials: true,
    baseURL: API_URL
})

api.interceptors.request.use((config) => {
    config.headers.Authorization = `Bearer ${localStorage.getItem('token')}`

    return config;
})

api.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response?.status === 500) {
        handleUnauthorized(); 
      }
      return Promise.reject(error);
    }
  );


export default api;
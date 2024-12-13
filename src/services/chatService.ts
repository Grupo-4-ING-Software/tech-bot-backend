import axios, { AxiosError } from 'axios';

const API_URL = 'http://localhost:8000/api';

const axiosInstance = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar el token
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (!token) {
    throw new Error('No authentication token found');
  }
  config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Interceptor para manejar errores
axiosInstance.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401 || error.response?.status === 403) {
      // Token inválido o expirado
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const getChatHistory = async () => {
  try {
    const response = await axiosInstance.get('/chat/history');
    return response.data;
  } catch (error) {
    if (error instanceof Error && error.message === 'No authentication token found') {
      window.location.href = '/login';
    }
    console.error('Error fetching chat history:', error);
    throw error;
  }
};

export const createChat = async (prompt: string) => {
  try {
    const response = await axiosInstance.post('/chat', { prompt });
    return response.data;
  } catch (error) {
    console.error('Error creating chat:', error);
    throw error;
  }
};

export const deleteChat = async (chatId: string) => {
  try {
    const response = await axiosInstance.delete(`/chat/${chatId}`);
    return response.data;
  } catch (error) {
    console.error('Error deleting chat:', error);
    throw error;
  }
};

// ... otros métodos del servicio 
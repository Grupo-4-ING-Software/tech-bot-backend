import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: {
    id: number;
    email: string;
  };
}

export const login = async (email: string, password: string) => {
  try {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await axios.post<LoginResponse>(`${API_URL}/token`, formData);
    
    // Guardar token y datos del usuario
    localStorage.setItem('token', response.data.access_token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    
    return response.data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
};

export const loginWithGoogle = async (googleToken: string) => {
  try {
    const response = await axios.post<LoginResponse>(`${API_URL}/login/google`, {
      token: googleToken
    });
    
    // Guardar token y datos del usuario
    localStorage.setItem('token', response.data.access_token);
    localStorage.setItem('user', JSON.stringify(response.data.user));
    
    return response.data;
  } catch (error) {
    console.error('Google login error:', error);
    throw error;
  }
}; 
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('sfms_access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('sfms_refresh_token');
      if (refreshToken) {
        try {
          const refreshResponse = await axios.post(`${api.defaults.baseURL}/auth/refresh`, { refresh_token: refreshToken });
          localStorage.setItem('sfms_access_token', refreshResponse.data.access_token);
          originalRequest.headers.Authorization = `Bearer ${refreshResponse.data.access_token}`;
          return axios(originalRequest);
        } catch {
          localStorage.removeItem('sfms_access_token');
          localStorage.removeItem('sfms_refresh_token');
        }
      }
    }
    return Promise.reject(error);
  },
);

export default api;

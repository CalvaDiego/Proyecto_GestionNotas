import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8080/', // URL del backend
});

// Interceptor para incluir el token JWT en las solicitudes
api.interceptors.request.use((config) => {
  if (!config.url.endsWith('/')) {
    config.url += '/'; // Asegura que todas las rutas incluyan la barra inclinada final
  }
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});


export default api;

import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.EXPO_PUBLIC_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 15000,
});

api.interceptors.request.use(async (config) => {
  const access = await AsyncStorage.getItem('accessToken');
  if (access) {
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      await AsyncStorage.multiRemove(['accessToken', 'refreshToken']);
    }
    return Promise.reject(error);
  },
);

export const saveTokens = async (tokens) => {
  if (!tokens) {
    return;
  }
  await AsyncStorage.multiSet([
    ['accessToken', tokens.access || ''],
    ['refreshToken', tokens.refresh || ''],
  ]);
};

export default api;

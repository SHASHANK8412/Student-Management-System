import api from './client';
import type { AuthResponse, AuthUser } from '@/types';

export async function login(email: string, password: string) {
  const { data } = await api.post<AuthResponse>('/auth/login', { email, password });
  return data;
}

export async function getCurrentUser() {
  const { data } = await api.get<AuthUser>('/auth/me');
  return data;
}

export async function logout(refresh_token: string) {
  await api.post('/auth/logout', { refresh_token });
}

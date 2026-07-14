import api from './client';
import type { DashboardResponse } from '@/types';

export async function getDashboard() {
  const { data } = await api.get<DashboardResponse>('/dashboard');
  return data;
}

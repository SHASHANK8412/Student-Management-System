import api from './client';
import type { Paginated } from './students';
import type { PaymentRecord } from '@/types';

export async function getPayments(params: { page: number; page_size: number; student_id?: number }) {
  const { data } = await api.get<Paginated<PaymentRecord>>('/payments', { params });
  return data;
}

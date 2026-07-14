import api from './client';
import type { FeeInvoiceRecord } from '@/types';
import type { Paginated } from './students';

export interface FeeInvoicePayload {
  student_id: number;
  fee_structure_id?: number | null;
  due_date: string;
  billing_period?: string | null;
  total_fee: number;
  scholarship_amount?: number;
  discount_amount?: number;
  late_fee?: number;
  amount_paid: number;
  balance_amount?: number;
  status?: string;
  notes?: string | null;
}

export async function getInvoices(params: { page: number; page_size: number; status?: string; student_id?: number }) {
  const { data } = await api.get<Paginated<FeeInvoiceRecord>>('/fees/invoices', { params });
  return data;
}

export async function createInvoice(payload: FeeInvoicePayload) {
  const { data } = await api.post<FeeInvoiceRecord>('/fees/invoices', payload);
  return data;
}

export async function updateInvoice(invoiceId: number, payload: Partial<FeeInvoicePayload>) {
  const { data } = await api.patch<FeeInvoiceRecord>(`/fees/invoices/${invoiceId}`, payload);
  return data;
}

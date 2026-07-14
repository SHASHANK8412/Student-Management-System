import api from './client';

export async function getAttendance(params: { page: number; page_size: number; student_id?: number }) {
  const { data } = await api.get('/attendance', { params });
  return data as { items: any[]; meta: { page: number; page_size: number; total: number; total_pages: number } };
}

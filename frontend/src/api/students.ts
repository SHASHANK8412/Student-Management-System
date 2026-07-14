import api from './client';
import type { StudentRecord } from '@/types';

export interface StudentCreatePayload {
  admission_number: string;
  student_name: string;
  class_name: string;
  parent_name?: string | null;
  date_of_birth?: string | null;
  aadhar_number?: string | null;
  pen_number?: string | null;
  caste?: string | null;
  sub_caste?: string | null;
  phone?: string | null;
  status?: string;
}

export interface StudentUpdatePayload {
  student_name?: string | null;
  class_name?: string | null;
  parent_name?: string | null;
  date_of_birth?: string | null;
  aadhar_number?: string | null;
  pen_number?: string | null;
  caste?: string | null;
  sub_caste?: string | null;
  phone?: string | null;
  status?: string | null;
}

export interface Paginated<T> {
  items: T[];
  meta: {
    page: number;
    page_size: number;
    total: number;
    total_pages: number;
  };
}

export async function getStudents(params: { page: number; page_size: number; search?: string }) {
  const { data } = await api.get<Paginated<StudentRecord>>('/students', { params });
  return data;
}

export async function getStudent(studentId: string) {
  const { data } = await api.get<StudentRecord>(`/students/${studentId}`);
  return data;
}

export async function createStudent(payload: StudentCreatePayload) {
  const { data } = await api.post<StudentRecord>('/students', payload);
  return data;
}

export async function updateStudent(studentId: number, payload: StudentUpdatePayload) {
  const { data } = await api.patch<StudentRecord>(`/students/${studentId}`, payload);
  return data;
}

export async function deleteStudent(studentId: number) {
  await api.delete(`/students/${studentId}`);
}

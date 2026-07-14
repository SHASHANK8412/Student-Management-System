import api from './client';

export async function getSchoolProfile() {
  const { data } = await api.get('/settings/school');
  return data as {
    id: number;
    school_name: string;
    logo_url?: string | null;
    address?: string | null;
    phone?: string | null;
    email?: string | null;
    currency: string;
    timezone: string;
    academic_year?: string | null;
    is_active: boolean;
  };
}

export async function getAcademicYears() {
  const { data } = await api.get('/settings/academic-years');
  return data as { id: number; name: string; start_date: string; end_date: string; is_active: boolean }[];
}

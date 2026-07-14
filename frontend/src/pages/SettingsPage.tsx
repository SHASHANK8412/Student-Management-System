import { useQuery } from '@tanstack/react-query';

import { getAcademicYears, getSchoolProfile } from '@/api/settings';
import { Card } from '@/components/ui/Card';
import { LoadingSkeleton } from '@/components/ui/LoadingSkeleton';

export function SettingsPage() {
  const school = useQuery({ queryKey: ['settings', 'school'], queryFn: getSchoolProfile });
  const years = useQuery({ queryKey: ['settings', 'years'], queryFn: getAcademicYears });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold">Admin Settings</h1>
        <p className="mt-2 text-sm text-slate-400">Manage school profile, academic years, and operational settings.</p>
      </div>
      {school.isLoading ? (
        <LoadingSkeleton className="h-40 w-full" />
      ) : (
        <Card>
          <h2 className="text-lg font-semibold">School Information</h2>
          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <div>School: {school.data?.school_name}</div>
            <div>Academic Year: {school.data?.academic_year ?? '-'}</div>
            <div>Phone: {school.data?.phone ?? '-'}</div>
            <div>Email: {school.data?.email ?? '-'}</div>
          </div>
        </Card>
      )}
      <Card>
        <h2 className="text-lg font-semibold">Academic Years</h2>
        <div className="mt-4 space-y-3">
          {years.data?.map((year) => <div key={year.id} className="rounded-2xl bg-white/5 px-4 py-3">{year.name} {year.is_active ? '(Active)' : ''}</div>)}
        </div>
      </Card>
    </div>
  );
}

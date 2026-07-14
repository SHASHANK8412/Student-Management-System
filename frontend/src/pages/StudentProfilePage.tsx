import { useQuery } from '@tanstack/react-query';
import { useParams } from 'react-router-dom';

import { getStudent } from '@/api/students';
import { Card } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { LoadingSkeleton } from '@/components/ui/LoadingSkeleton';

export function StudentProfilePage() {
  const { studentId = '' } = useParams();
  const { data, isLoading } = useQuery({ queryKey: ['student', studentId], queryFn: () => getStudent(studentId), enabled: Boolean(studentId) });

  if (isLoading || !data) {
    return <LoadingSkeleton className="h-80 w-full" />;
  }

  const fields = [
    ['Admission Number', data.admission_number],
    ['Class', `${data.class_name} ${data.section ?? ''}`],
    ['Roll Number', data.roll_number ?? '-'],
    ['Date of Birth', data.date_of_birth ?? '-'],
    ['Phone', data.phone ?? '-'],
    ['Aadhar Number', data.aadhar_number ?? '-'],
    ['PEN Number', data.pen_number ?? '-'],
    ['Email', data.email ?? '-'],
    ['Father', data.father_name ?? '-'],
    ['Parent', data.parent_name ?? data.father_name ?? '-'],
    ['Mother', data.mother_name ?? '-'],
    ['Caste', data.caste ?? '-'],
    ['Sub Caste', data.sub_caste ?? '-'],
    ['Status', data.status],
  ];

  return (
    <div className="space-y-6">
      <Card className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-sm text-slate-400">Student Profile</p>
          <h1 className="mt-1 text-3xl font-semibold">{data.student_name}</h1>
        </div>
        <Badge tone={data.status === 'Active' ? 'success' : 'warning'}>{data.status}</Badge>
      </Card>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {fields.map(([label, value]) => (
          <Card key={label}>
            <p className="text-xs uppercase tracking-[0.2em] text-slate-400">{label}</p>
            <p className="mt-2 text-lg font-medium">{value}</p>
          </Card>
        ))}
      </div>
    </div>
  );
}

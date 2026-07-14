import { useQuery } from '@tanstack/react-query';
import { getAttendance } from '@/api/attendance';
import { Card } from '@/components/ui/Card';
import { LoadingSkeleton } from '@/components/ui/LoadingSkeleton';
import { Badge } from '@/components/ui/Badge';

export function AttendancePage() {
  const { data, isLoading } = useQuery({ queryKey: ['attendance'], queryFn: () => getAttendance({ page: 1, page_size: 20 }) });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold">Attendance</h1>
        <p className="mt-2 text-sm text-slate-400">Daily and monthly attendance snapshots.</p>
      </div>
      {isLoading ? (
        <LoadingSkeleton className="h-80 w-full" />
      ) : (
        <div className="grid gap-4 xl:grid-cols-2">
          {data?.items.map((record) => (
            <Card key={record.id} className="flex items-center justify-between">
              <div>
                <p className="font-semibold">Student #{record.student_id}</p>
                <p className="text-sm text-slate-400">{record.attendance_date}</p>
              </div>
              <Badge tone={record.status === 'Present' ? 'success' : record.status === 'Absent' ? 'danger' : 'warning'}>{record.status}</Badge>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

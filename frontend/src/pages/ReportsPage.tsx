import { useQuery } from '@tanstack/react-query';
import { Download } from 'lucide-react';

import { getCollectionReport, getPendingFeesReport } from '@/api/reports';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';

export function ReportsPage() {
  const collection = useQuery({ queryKey: ['reports', 'collection'], queryFn: getCollectionReport });
  const pending = useQuery({ queryKey: ['reports', 'pending'], queryFn: getPendingFeesReport });

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 className="text-3xl font-semibold">Reports</h1>
          <p className="mt-2 text-sm text-slate-400">Collection, pending fees, class-wise summaries, and ledger exports.</p>
        </div>
        <div className="flex gap-3">
          <Button variant="secondary"><Download className="h-4 w-4" /> <span className="ml-2">PDF</span></Button>
          <Button variant="secondary"><Download className="h-4 w-4" /> <span className="ml-2">Excel</span></Button>
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <p className="text-sm text-slate-400">Total Collection</p>
          <p className="mt-2 text-3xl font-semibold">{collection.data?.total_collection?.toLocaleString() ?? '0'}</p>
        </Card>
        <Card>
          <p className="text-sm text-slate-400">Pending Fees</p>
          <p className="mt-2 text-3xl font-semibold">{pending.data?.pending_fees?.toLocaleString() ?? '0'}</p>
        </Card>
      </div>
    </div>
  );
}

import { useQuery } from '@tanstack/react-query';
import { getPayments } from '@/api/payments';
import { Card } from '@/components/ui/Card';
import { LoadingSkeleton } from '@/components/ui/LoadingSkeleton';
import { Badge } from '@/components/ui/Badge';

export function PaymentsPage() {
  const { data, isLoading } = useQuery({ queryKey: ['payments'], queryFn: () => getPayments({ page: 1, page_size: 20 }) });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold">Payments</h1>
        <p className="mt-2 text-sm text-slate-400">Track receipts, modes, and payment histories.</p>
      </div>
      {isLoading ? (
        <LoadingSkeleton className="h-80 w-full" />
      ) : (
        <div className="grid gap-4 xl:grid-cols-2">
          {data?.items.map((payment) => (
            <Card key={payment.id} className="space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold">{payment.receipt_number}</h3>
                <Badge tone="info">{payment.payment_mode}</Badge>
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm text-slate-300">
                <div>Amount: {payment.amount}</div>
                <div>Date: {payment.payment_date}</div>
                <div>Reference: {payment.reference_number ?? '-'}</div>
                <div>Remarks: {payment.remarks ?? '-'}</div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

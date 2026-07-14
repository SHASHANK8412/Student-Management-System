import { useQuery } from '@tanstack/react-query';
import { getInvoices } from '@/api/fees';
import { Card } from '@/components/ui/Card';
import { LoadingSkeleton } from '@/components/ui/LoadingSkeleton';
import { Badge } from '@/components/ui/Badge';

export function FeesPage() {
  const { data, isLoading } = useQuery({ queryKey: ['fees', 'invoices'], queryFn: () => getInvoices({ page: 1, page_size: 20 }) });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-semibold">Fee Structures & Invoices</h1>
        <p className="mt-2 text-sm text-slate-400">Manage balances, installments, and payment status.</p>
      </div>
      {isLoading ? (
        <LoadingSkeleton className="h-80 w-full" />
      ) : (
        <div className="grid gap-4 xl:grid-cols-2">
          {data?.items.map((invoice) => (
            <Card key={invoice.id} className="space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold">{invoice.invoice_number}</h3>
                <Badge tone={invoice.status === 'Paid' ? 'success' : invoice.status === 'Partial' ? 'warning' : 'danger'}>{invoice.status}</Badge>
              </div>
              <div className="grid grid-cols-2 gap-3 text-sm text-slate-300">
                <div>Total: {invoice.total_fee}</div>
                <div>Paid: {invoice.amount_paid}</div>
                <div>Balance: {invoice.balance_amount}</div>
                <div>Due: {invoice.due_date}</div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

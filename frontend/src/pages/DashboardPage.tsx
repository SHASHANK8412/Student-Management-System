import { useQuery } from '@tanstack/react-query';
import { motion } from 'framer-motion';
import { TrendingUp, Users, Wallet, AlertCircle, CalendarClock, BadgeDollarSign } from 'lucide-react';

import { getDashboard } from '@/api/dashboard';
import { Card } from '@/components/ui/Card';
import { LoadingSkeleton } from '@/components/ui/LoadingSkeleton';
import { SummaryChart } from '@/components/charts/SummaryChart';
import { Badge } from '@/components/ui/Badge';

const statItems = [
  { label: 'Total Students', icon: Users, valueKey: 'total_students' },
  { label: 'Active Students', icon: BadgeDollarSign, valueKey: 'active_students' },
  { label: 'Total Collection', icon: Wallet, valueKey: 'total_collection' },
  { label: 'Pending Fees', icon: AlertCircle, valueKey: 'pending_fees' },
  { label: "Today's Collection", icon: TrendingUp, valueKey: 'todays_collection' },
  { label: 'Monthly Revenue', icon: CalendarClock, valueKey: 'monthly_revenue' },
];

export function DashboardPage() {
  const { data, isLoading } = useQuery({ queryKey: ['dashboard'], queryFn: getDashboard });

  if (isLoading || !data) {
    return <LoadingSkeleton className="h-96 w-full" />;
  }

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {statItems.map((item) => {
          const Icon = item.icon;
          const value = data.kpi[item.valueKey as keyof typeof data.kpi] as number;
          return (
            <Card key={item.label} className="flex items-center justify-between gap-4">
              <div>
                <p className="text-sm text-slate-400">{item.label}</p>
                <h3 className="mt-2 text-3xl font-semibold">{typeof value === 'number' ? value.toLocaleString() : value}</h3>
              </div>
              <div className="rounded-2xl bg-sky-500/15 p-4 text-sky-300">
                <Icon className="h-6 w-6" />
              </div>
            </Card>
          );
        })}
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.5fr,1fr]">
        <SummaryChart data={data.monthly_collection} />
        <Card>
          <h3 className="text-base font-semibold">Upcoming Due Dates</h3>
          <div className="mt-4 space-y-3">
            {data.upcoming_due_dates.length ? data.upcoming_due_dates.map((item) => <Badge key={item} tone="warning" className="w-full justify-between rounded-2xl py-3">{item}</Badge>) : <p className="text-sm text-slate-400">No upcoming dues right now.</p>}
          </div>
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-3">
        <Card>
          <h3 className="text-base font-semibold">Class-wise Revenue</h3>
          <div className="mt-4 space-y-3">
            {data.class_wise_revenue.map((entry) => (
              <div key={entry.label} className="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3">
                <span>{entry.label}</span>
                <span className="text-sky-300">{entry.value.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </Card>
        <Card>
          <h3 className="text-base font-semibold">Due Distribution</h3>
          <div className="mt-4 space-y-3">
            {data.due_distribution.map((entry) => (
              <div key={entry.label} className="flex items-center justify-between rounded-2xl bg-white/5 px-4 py-3">
                <span>{entry.label}</span>
                <span>{entry.value.toLocaleString()}</span>
              </div>
            ))}
          </div>
        </Card>
        <Card>
          <h3 className="text-base font-semibold">Recent Activity</h3>
          <div className="mt-4 space-y-3 text-sm text-slate-300">
            {data.recent_activity.length ? data.recent_activity.map((item) => <p key={item} className="rounded-2xl bg-white/5 px-4 py-3">{item}</p>) : <p className="text-slate-400">No recent activity.</p>}
          </div>
        </Card>
      </div>
    </motion.div>
  );
}

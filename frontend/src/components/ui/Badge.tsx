import { cn } from '@/lib/cn';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  tone?: 'success' | 'warning' | 'danger' | 'info' | 'neutral';
}

export function Badge({ className, tone = 'neutral', ...props }: BadgeProps) {
  const tones = {
    success: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/20',
    warning: 'bg-amber-500/15 text-amber-300 border-amber-500/20',
    danger: 'bg-rose-500/15 text-rose-300 border-rose-500/20',
    info: 'bg-sky-500/15 text-sky-300 border-sky-500/20',
    neutral: 'bg-white/10 text-slate-200 border-white/10',
  };

  return <span className={cn('inline-flex items-center rounded-full border px-3 py-1 text-xs font-medium', tones[tone], className)} {...props} />;
}

import { cn } from '@/lib/cn';

export function Input({ className, ...props }: React.InputHTMLAttributes<HTMLInputElement>) {
  return <input className={cn('w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-inherit outline-none transition placeholder:text-slate-400 focus:border-brand-400 focus:bg-white/10', className)} {...props} />;
}

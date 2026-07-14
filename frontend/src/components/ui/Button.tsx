import { cn } from '@/lib/cn';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
}

export function Button({ className, variant = 'primary', ...props }: ButtonProps) {
  const styles = {
    primary: 'bg-brand-500 text-white shadow-glass hover:bg-brand-400',
    secondary: 'bg-white/10 text-white border border-white/10 hover:bg-white/15',
    ghost: 'bg-transparent text-inherit hover:bg-white/10',
  };

  return <button className={cn('inline-flex items-center justify-center rounded-2xl px-4 py-2 text-sm font-semibold transition', styles[variant], className)} {...props} />;
}

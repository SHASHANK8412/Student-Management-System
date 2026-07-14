import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { motion } from 'framer-motion';
import toast from 'react-hot-toast';
import { GraduationCap, ShieldCheck } from 'lucide-react';

import * as authApi from '@/api/auth';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { useAuth } from '@/context/auth-context';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

type FormValues = z.infer<typeof schema>;

export function LoginPage() {
  const { login } = useAuth();
  const [submitting, setSubmitting] = useState(false);
  const demoEmail = 'admin@westsideacademy.com';
  const demoPassword = 'Admin@1234';
  const { register, handleSubmit, setValue, formState: { errors } } = useForm<FormValues>({ resolver: zodResolver(schema) });

  const useDemoCredentials = () => {
    setValue('email', demoEmail, { shouldValidate: true });
    setValue('password', demoPassword, { shouldValidate: true });
  };

  const onSubmit = handleSubmit(async (values) => {
    setSubmitting(true);
    try {
      const response = await authApi.login(values.email, values.password);
      login(response);
      toast.success('Logged in successfully');
    } catch {
      toast.error('Invalid email or password');
    } finally {
      setSubmitting(false);
    }
  });

  return (
    <div className="grid min-h-screen grid-cols-1 lg:grid-cols-2">
      <div className="flex items-center justify-center px-6 py-14">
        <motion.div initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.45 }} className="w-full max-w-md">
          <Card className="space-y-6">
            <div className="flex items-center gap-3">
              <div className="rounded-2xl bg-sky-500/20 p-3">
                <GraduationCap className="h-6 w-6 text-sky-300" />
              </div>
              <div>
                <p className="text-sm text-slate-400">Westside Academy</p>
                <h1 className="font-display text-2xl font-bold">Fee Console</h1>
              </div>
            </div>
            <div>
              <h2 className="text-3xl font-semibold">Secure login</h2>
              <p className="mt-2 text-sm text-slate-400">Access student accounts, fees, and collections from one secure workspace.</p>
            </div>
            <form className="space-y-4" onSubmit={onSubmit}>
              <div>
                <label className="mb-2 block text-sm font-medium">Email</label>
                <Input type="email" placeholder="admin@school.edu" {...register('email')} />
                {errors.email ? <p className="mt-1 text-xs text-rose-300">{errors.email.message}</p> : null}
              </div>
              <div>
                <label className="mb-2 block text-sm font-medium">Password</label>
                <Input type="password" placeholder="••••••••" {...register('password')} />
                {errors.password ? <p className="mt-1 text-xs text-rose-300">{errors.password.message}</p> : null}
              </div>
              <Button type="submit" className="w-full" disabled={submitting}>
                {submitting ? 'Signing in...' : 'Login'}
              </Button>
            </form>
            <div className="space-y-3 rounded-2xl border border-slate-700/70 bg-slate-950/40 p-4">
              <div>
                <p className="text-sm font-semibold text-slate-100">Demo credentials</p>
                <p className="mt-1 text-xs text-slate-400">Use these to access the dashboard right away.</p>
              </div>
              <div className="grid gap-2 text-sm text-slate-200">
                <div className="flex items-center justify-between gap-4 rounded-xl bg-slate-900/70 px-3 py-2">
                  <span className="text-slate-400">Email</span>
                  <span className="font-medium">{demoEmail}</span>
                </div>
                <div className="flex items-center justify-between gap-4 rounded-xl bg-slate-900/70 px-3 py-2">
                  <span className="text-slate-400">Password</span>
                  <span className="font-medium">{demoPassword}</span>
                </div>
              </div>
              <Button type="button" variant="secondary" className="w-full" onClick={useDemoCredentials}>
                Use demo credentials
              </Button>
            </div>
            <div className="flex items-center gap-3 rounded-2xl border border-sky-500/20 bg-sky-500/10 p-4 text-sm text-sky-100">
              <ShieldCheck className="h-5 w-5" />
              JWT authentication, refresh tokens, RBAC, and audit-ready flows.
            </div>
          </Card>
        </motion.div>
      </div>
      <div className="relative hidden overflow-hidden p-10 lg:flex">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(14,165,233,0.28),transparent_32%),linear-gradient(180deg,rgba(2,6,23,0.2),rgba(2,6,23,0.9))]" />
        <div className="relative z-10 flex max-w-xl flex-col justify-end gap-6">
          <h2 className="font-display text-5xl font-bold leading-tight">A modern fee management system built for real operations.</h2>
          <p className="text-lg text-slate-300">Track collections, due dates, attendance, and reports with a secure dashboard designed for school finance teams.</p>
        </div>
      </div>
    </div>
  );
}

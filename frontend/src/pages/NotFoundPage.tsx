import { Link } from 'react-router-dom';

export function NotFoundPage() {
  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center text-center">
      <p className="text-sm uppercase tracking-[0.3em] text-sky-300">404</p>
      <h1 className="mt-4 text-4xl font-semibold">Page not found</h1>
      <p className="mt-3 max-w-md text-slate-400">The route you requested does not exist in the fee management workspace.</p>
      <Link to="/" className="mt-8 rounded-2xl bg-sky-500 px-5 py-3 text-sm font-semibold text-white">Return to dashboard</Link>
    </div>
  );
}

import { Bell, MoonStar, SunMedium, LogOut } from 'lucide-react';
import { useAuth } from '@/context/auth-context';
import { useTheme } from '@/context/theme-context';
import { Button } from '@/components/ui/Button';

export function Header() {
  const { user, signOut } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="sticky top-0 z-20 flex items-center justify-between border-b border-white/10 bg-slate-950/50 px-4 py-4 backdrop-blur-xl md:px-6">
      <div>
        <p className="text-xs uppercase tracking-[0.2em] text-sky-300">Student Fee Management System</p>
        <h2 className="mt-1 text-lg font-semibold text-white">Welcome back, {user?.full_name ?? 'User'}</h2>
      </div>
      <div className="flex items-center gap-3">
        <Button variant="secondary" onClick={toggleTheme} aria-label="Toggle theme">
          {theme === 'dark' ? <SunMedium className="h-4 w-4" /> : <MoonStar className="h-4 w-4" />}
        </Button>
        <Button variant="secondary">
          <Bell className="h-4 w-4" />
        </Button>
        <Button variant="secondary" onClick={signOut}>
          <LogOut className="h-4 w-4" />
          <span className="ml-2 hidden sm:inline">Logout</span>
        </Button>
      </div>
    </header>
  );
}

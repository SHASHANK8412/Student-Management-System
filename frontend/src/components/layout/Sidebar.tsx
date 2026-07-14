import { NavLink } from 'react-router-dom';
import { LayoutDashboard, GraduationCap, LineChart, Settings, Users2 } from 'lucide-react';

const navItems = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/students', label: 'Students', icon: GraduationCap },
  { to: '/reports', label: 'Reports', icon: LineChart },
  { to: '/settings', label: 'Admin', icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="hidden w-72 flex-col border-r border-white/10 bg-slate-950/60 px-4 py-5 backdrop-blur-xl lg:flex">
      <div className="mb-8 rounded-3xl border border-white/10 bg-gradient-to-br from-sky-500/20 to-cyan-400/10 p-5">
        <div className="flex items-center gap-3">
          <div className="rounded-2xl bg-white/10 p-3">
            <Users2 className="h-6 w-6 text-sky-300" />
          </div>
          <div>
            <p className="text-sm text-slate-300">Westside Academy</p>
            <h1 className="font-display text-xl font-bold text-white">Fee Console</h1>
          </div>
        </div>
      </div>
      <nav className="space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-medium transition ${isActive ? 'bg-white/10 text-white' : 'text-slate-300 hover:bg-white/5 hover:text-white'}`
              }
            >
              <Icon className="h-4 w-4" />
              {item.label}
            </NavLink>
          );
        })}
      </nav>
      <div className="mt-auto rounded-3xl border border-white/10 bg-white/5 p-4 text-sm text-slate-300">
        Secure, auditable, and responsive fee management.
      </div>
    </aside>
  );
}

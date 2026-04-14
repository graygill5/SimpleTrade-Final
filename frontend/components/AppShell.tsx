'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useAuth } from './AuthProvider';
import { AssistantWidget } from './AssistantWidget';

const nav = [
  { href: '/dashboard/market', label: 'Market' },
  { href: '/dashboard/chat', label: 'Community Chat' },
  { href: '/dashboard/portfolio', label: 'Portfolio' },
  { href: '/dashboard/learning', label: 'Learning' }
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { logout } = useAuth();
  const router = useRouter();

  return (
    <div className="min-h-screen grid grid-cols-[220px_1fr]">
      <aside className="border-r border-borderc bg-panel p-4">
        <h1 className="text-xl font-bold mb-4">SimpleTrade</h1>
        <nav className="space-y-1">
          {nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`block rounded px-2 py-2 ${pathname === item.href ? 'bg-slate-800 text-accent' : 'text-slate-200'}`}
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <button
          className="mt-6 w-full rounded bg-slate-800 px-3 py-2 hover:bg-slate-700"
          onClick={() => {
            logout();
            router.push('/auth/login');
          }}
        >
          Logout
        </button>
      </aside>
      <main className="p-6 relative">
        <div className="flex justify-between items-center mb-6">
          <input className="card w-80" placeholder="Search tickers, users, chats, lessons..." />
          <div className="text-sm text-slate-400">SimpleTrade MVP Dashboard</div>
        </div>
        {children}
      </main>
      <AssistantWidget />
    </div>
  );
}

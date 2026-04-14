'use client';

import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { useAuth } from './AuthProvider';

export function Protected({ children }: { children: React.ReactNode }) {
  const { token } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!token) router.push('/auth/login');
  }, [token, router]);

  if (!token) return <div className="card">Checking authentication...</div>;
  return <>{children}</>;
}

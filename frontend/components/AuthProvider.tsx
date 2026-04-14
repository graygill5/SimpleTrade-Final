'use client';

import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import { apiGet, apiPost } from '@/lib/api';

type Tokens = { access_token: string; refresh_token: string };

type AuthCtx = {
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
};

const Ctx = createContext<AuthCtx | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    setToken(localStorage.getItem('access_token'));
  }, []);


  const hydrateUser = async (access: string) => {
    try {
      const me = await apiGet('/social/me', access);
      localStorage.setItem('user_id', String(me.id));
    } catch {
      // ignore hydration errors during MVP flow
    }
  };

  const save = (pair: Tokens) => {
    localStorage.setItem('access_token', pair.access_token);
    localStorage.setItem('refresh_token', pair.refresh_token);
    setToken(pair.access_token);
    hydrateUser(pair.access_token);
  };

  const login = async (email: string, password: string) => {
    const pair = await apiPost('/auth/login', { email, password });
    save(pair);
  };

  const signup = async (username: string, email: string, password: string) => {
    const pair = await apiPost('/auth/signup', { username, email, password });
    save(pair);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setToken(null);
  };

  const value = useMemo(() => ({ token, login, signup, logout }), [token]);
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useAuth() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}

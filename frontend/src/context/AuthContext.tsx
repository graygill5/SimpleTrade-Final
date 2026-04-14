import React, { createContext, useContext, useMemo, useState } from 'react';
import { apiPost } from '../services/api';

type AuthContextType = {
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  signup: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));

  async function login(email: string, password: string) {
    const data = await apiPost('/auth/login', { email, password });
    localStorage.setItem('token', data.access_token);
    setToken(data.access_token);
  }

  async function signup(username: string, email: string, password: string) {
    const data = await apiPost('/auth/signup', { username, email, password });
    localStorage.setItem('token', data.access_token);
    setToken(data.access_token);
  }

  function logout() {
    localStorage.removeItem('token');
    setToken(null);
  }

  const value = useMemo(() => ({ token, login, signup, logout }), [token]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('AuthContext not initialized');
  return ctx;
}

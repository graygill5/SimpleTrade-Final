'use client';

import { FormEvent, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/AuthProvider';

export default function LoginPage() {
  const { login } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState('demo@simpletrade.dev');
  const [password, setPassword] = useState('demo1234');
  const [error, setError] = useState('');

  async function submit(e: FormEvent) {
    e.preventDefault();
    setError('');
    try {
      await login(email, password);
      router.push('/dashboard/market');
    } catch {
      setError('Login failed.');
    }
  }

  return (
    <main className="min-h-screen grid place-items-center">
      <form onSubmit={submit} className="card w-full max-w-md space-y-3">
        <h1 className="text-2xl font-bold">Login</h1>
        <input className="card w-full" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="card w-full" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        {error && <p className="text-red-400">{error}</p>}
        <button className="w-full rounded bg-accent text-black px-3 py-2 font-semibold">Login</button>
      </form>
    </main>
  );
}

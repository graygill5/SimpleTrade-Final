'use client';

import { FormEvent, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/components/AuthProvider';

export default function SignupPage() {
  const { signup } = useAuth();
  const router = useRouter();
  const [username, setUsername] = useState('newuser');
  const [email, setEmail] = useState('new@simpletrade.dev');
  const [password, setPassword] = useState('demo1234');

  async function submit(e: FormEvent) {
    e.preventDefault();
    await signup(username, email, password);
    router.push('/dashboard/market');
  }

  return (
    <main className="min-h-screen grid place-items-center">
      <form onSubmit={submit} className="card w-full max-w-md space-y-3">
        <h1 className="text-2xl font-bold">Create account</h1>
        <input className="card w-full" value={username} onChange={(e) => setUsername(e.target.value)} />
        <input className="card w-full" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input className="card w-full" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button className="w-full rounded bg-accent text-black px-3 py-2 font-semibold">Sign up</button>
      </form>
    </main>
  );
}

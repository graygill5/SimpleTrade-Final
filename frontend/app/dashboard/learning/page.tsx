'use client';

import { useEffect, useState } from 'react';
import { apiGet, apiPost } from '@/lib/api';
import { useAuth } from '@/components/AuthProvider';

export default function LearningPage() {
  const { token } = useAuth();
  const [modules, setModules] = useState<any[]>([]);
  const [progress, setProgress] = useState<any>(null);

  async function load() {
    if (!token) return;
    setModules(await apiGet('/learning/modules', token));
    setProgress(await apiGet('/learning/progress', token));
  }

  useEffect(() => { load(); }, [token]);

  async function complete(moduleId: number) {
    if (!token) return;
    await apiPost('/learning/complete', { module_id: moduleId, score: 90 }, token);
    await load();
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold">Learning Modules</h2>
      <div className="grid md:grid-cols-3 gap-3">
        <div className="card">XP: {progress?.xp || 0}</div>
        <div className="card">Level: {progress?.level || 1}</div>
        <div className="card">Completed: {progress?.completed?.length || 0}</div>
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        {modules.map((m) => (
          <div key={m.id} className="card">
            <h3 className="font-semibold">{m.title}</h3>
            <p className="text-sm text-slate-400">{m.description}</p>
            <p className="my-2">{m.content}</p>
            <button className="rounded bg-slate-700 px-3 py-1" onClick={() => complete(m.id)}>Complete + Reward</button>
          </div>
        ))}
      </div>
    </div>
  );
}

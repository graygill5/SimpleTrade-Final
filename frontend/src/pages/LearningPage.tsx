import { useEffect, useState } from 'react';
import { apiGet, apiPost } from '../services/api';

export function LearningPage() {
  const [modules, setModules] = useState<any[]>([]);

  useEffect(() => {
    apiGet('/learning/modules').then(setModules).catch(() => setModules([]));
  }, []);

  async function complete(moduleId: number) {
    await apiPost('/learning/complete', { module_id: moduleId, quiz_score: 90 });
    alert('Module completed! XP and virtual cash reward granted.');
  }

  return (
    <section>
      <h2>Learning Modules</h2>
      <p>Lessons, quiz completion tracking, XP, and in-app rewards funding paper trades.</p>
      <div className="grid">
        {modules.map((m) => (
          <article className="panel" key={m.id}>
            <h3>{m.title}</h3>
            <p>{m.content}</p>
            <p>XP Reward: {m.xp_reward}</p>
            <button onClick={() => complete(m.id)}>Complete + Reward</button>
          </article>
        ))}
      </div>
    </section>
  );
}

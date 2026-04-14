'use client';

import { useState } from 'react';
import { apiGet, apiPost } from '@/lib/api';
import { useAuth } from './AuthProvider';

export function AssistantWidget() {
  const [open, setOpen] = useState(true);
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const { token } = useAuth();

  async function send() {
    if (!question.trim() || !token) return;
    const userMsg = { role: 'user', content: question };
    setMessages((m) => [...m, userMsg]);
    const res = await apiPost('/assistant/ask', { question, page: window.location.pathname }, token);
    setMessages((m) => [...m, { role: 'assistant', content: res.answer }]);
    setQuestion('');
  }

  async function loadHistory() {
    if (!token) return;
    const rows = await apiGet('/assistant/history', token);
    setMessages(rows.map((r: any) => ({ role: r.role, content: r.content })));
  }

  return (
    <div className="fixed right-4 bottom-4 w-80">
      <button className="w-full rounded-t-xl bg-accent text-black px-3 py-2 font-semibold" onClick={() => setOpen((o) => !o)}>
        AI Coach {open ? '▼' : '▲'}
      </button>
      {open && (
        <div className="card rounded-t-none space-y-2">
          <div className="flex gap-2">
            <button className="text-xs underline" onClick={loadHistory}>Load history</button>
            <span className="text-xs text-slate-400">Try: "Why is my portfolio down?"</span>
          </div>
          <div className="max-h-44 overflow-y-auto space-y-2 text-sm">
            {messages.map((m, idx) => (
              <div key={idx} className={m.role === 'assistant' ? 'text-cyan-300' : 'text-slate-200'}>{m.role}: {m.content}</div>
            ))}
          </div>
          <textarea className="w-full card" value={question} onChange={(e) => setQuestion(e.target.value)} />
          <button className="rounded bg-slate-700 px-3 py-2 w-full" onClick={send}>Ask</button>
        </div>
      )}
    </div>
  );
}

'use client';

import { useEffect, useState } from 'react';
import { apiGet } from '@/lib/api';
import { useAuth } from '@/components/AuthProvider';

export default function ChatPage() {
  const { token } = useAuth();
  const [rooms, setRooms] = useState<any[]>([]);
  const [roomId, setRoomId] = useState<number | null>(null);
  const [messages, setMessages] = useState<any[]>([]);
  const [text, setText] = useState('');
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    if (!token) return;
    apiGet('/chat/rooms', token).then(setRooms);
  }, [token]);

  useEffect(() => {
    if (!roomId) return;
    const userId = Number(localStorage.getItem('user_id') || 1);
    const socket = new WebSocket(`${(process.env.NEXT_PUBLIC_WS_BASE || 'ws://localhost:8000')}/api/v1/chat/ws/${roomId}/${userId}`);
    socket.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.type === 'message') setMessages((prev) => [...prev, data]);
    };
    setWs(socket);
    return () => socket.close();
  }, [roomId]);

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold">Community Chat</h2>
      <div className="grid md:grid-cols-[240px_1fr] gap-4">
        <div className="card space-y-2">
          {rooms.map((r) => <button key={r.id} className="block underline" onClick={() => setRoomId(r.id)}>{r.name}</button>)}
        </div>
        <div className="card">
          <div className="h-80 overflow-y-auto space-y-1 mb-3">
            {messages.map((m, i) => <div key={i}><b>U{m.sender_id}</b>: {m.body}</div>)}
          </div>
          <div className="flex gap-2">
            <input className="card flex-1" value={text} onChange={(e) => setText(e.target.value)} onKeyDown={() => ws?.send(JSON.stringify({ type: 'typing' }))} />
            <button className="rounded bg-slate-700 px-3" onClick={() => { ws?.send(JSON.stringify({ type: 'message', body: text })); setText(''); }}>Send</button>
          </div>
        </div>
      </div>
    </div>
  );
}

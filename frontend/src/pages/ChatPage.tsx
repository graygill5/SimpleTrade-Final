import { useEffect, useState } from 'react';

export function ChatPage() {
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [messages, setMessages] = useState<string[]>([]);
  const [text, setText] = useState('');

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/api/v1/chat/ws/global');
    socket.onmessage = (event) => setMessages((prev) => [...prev, event.data]);
    setWs(socket);
    return () => socket.close();
  }, []);

  function send() {
    if (!text.trim() || !ws) return;
    ws.send(text);
    setText('');
  }

  return (
    <section>
      <h2>Community Chat</h2>
      <p>Global chat with room-based WebSocket plumbing. DM/group/friends APIs can extend this layer.</p>
      <div className="panel chat-log">
        {messages.map((m, i) => (
          <p key={i}>{m}</p>
        ))}
      </div>
      <div className="row">
        <input value={text} onChange={(e) => setText(e.target.value)} placeholder="Share a market thought..." />
        <button onClick={send}>Send</button>
      </div>
    </section>
  );
}

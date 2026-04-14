import { useState } from 'react';
import { apiPost } from '../services/api';

export function AiWidget() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('Ask me about your portfolio, market, or learning progress.');

  async function ask() {
    if (!question.trim()) return;
    try {
      const res = await apiPost('/assistant/ask', { question });
      setAnswer(res.answer);
    } catch {
      setAnswer('Assistant unavailable right now.');
    }
  }

  return (
    <div className="ai-widget">
      <h3>AI Assistant</h3>
      <textarea value={question} onChange={(e) => setQuestion(e.target.value)} />
      <button onClick={ask}>Ask</button>
      <p>{answer}</p>
    </div>
  );
}

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api/v1';

function authHeaders() {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function apiGet(path: string) {
  const res = await fetch(`${API_BASE}${path}`, { headers: { ...authHeaders() } });
  if (!res.ok) throw new Error(`GET ${path} failed`);
  return res.json();
}

export async function apiPost(path: string, body: object) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeaders() },
    body: JSON.stringify(body)
  });
  if (!res.ok) throw new Error(`POST ${path} failed`);
  return res.json();
}

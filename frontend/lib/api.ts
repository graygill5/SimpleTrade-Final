const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api/v1';

export async function apiGet(path: string, token?: string | null) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    cache: 'no-store',
  });
  if (!res.ok) throw new Error(`GET failed: ${path}`);
  return res.json();
}

export async function apiPost(path: string, body: unknown, token?: string | null) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`POST failed: ${path}`);
  return res.json();
}

export async function apiDelete(path: string, token?: string | null) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: 'DELETE',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error(`DELETE failed: ${path}`);
  return res.json();
}

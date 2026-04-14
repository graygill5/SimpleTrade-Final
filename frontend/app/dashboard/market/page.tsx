'use client';

import { useEffect, useState } from 'react';
import { apiGet, apiPost, apiDelete } from '@/lib/api';
import { useAuth } from '@/components/AuthProvider';

export default function MarketPage() {
  const [overview, setOverview] = useState<any>(null);
  const [q, setQ] = useState('NVDA');
  const [results, setResults] = useState<any[]>([]);
  const [asset, setAsset] = useState<any>(null);
  const { token } = useAuth();

  useEffect(() => {
    if (!token) return;
    apiGet('/market/overview', token).then(setOverview);
  }, [token]);

  async function search() {
    if (!token) return;
    setResults(await apiGet(`/market/search?q=${encodeURIComponent(q)}`, token));
  }

  async function loadAsset(symbol: string) {
    if (!token) return;
    setAsset(await apiGet(`/market/asset/${symbol}`, token));
  }

  async function save(symbol: string) { if (token) await apiPost(`/market/watchlist/${symbol}`, {}, token); }
  async function unsave(symbol: string) { if (token) await apiDelete(`/market/watchlist/${symbol}`, token); }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold">Market Overview</h2>
      <div className="card grid md:grid-cols-3 gap-3">
        {overview?.indexes?.map((i: any) => <div key={i.symbol}><b>{i.name}</b><p>{i.change_pct}%</p></div>)}
      </div>
      <div className="card">
        <p>{overview?.summary}</p>
      </div>
      <div className="card flex gap-2">
        <input className="card flex-1" value={q} onChange={(e) => setQ(e.target.value)} />
        <button className="rounded bg-slate-700 px-3" onClick={search}>Search</button>
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        <div className="card space-y-2">
          {results.map((r) => (
            <div key={r.symbol} className="flex justify-between">
              <button className="underline" onClick={() => loadAsset(r.symbol)}>{r.symbol} - {r.name}</button>
              <div className="space-x-2"><button onClick={() => save(r.symbol)}>☆</button><button onClick={() => unsave(r.symbol)}>✕</button></div>
            </div>
          ))}
        </div>
        <div className="card">
          {asset ? (
            <div className="space-y-1">
              <h3 className="text-xl font-bold">{asset.symbol} - {asset.name}</h3>
              <p>Price: ${asset.price} ({asset.change_pct}%)</p>
              <p>Volume: {asset.volume}</p>
              <p>Outlook: {asset.outlook}</p>
              <p className="text-cyan-200">Why This Matters: {asset.why_this_matters}</p>
            </div>
          ) : <p>Select an asset.</p>}
        </div>
      </div>
    </div>
  );
}

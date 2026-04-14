'use client';

import { useEffect, useState } from 'react';
import { PieChart, Pie, Cell, Tooltip } from 'recharts';
import { apiGet, apiPost } from '@/lib/api';
import { useAuth } from '@/components/AuthProvider';

const colors = ['#42d3ff', '#8892ff', '#4ade80', '#f59e0b'];

export default function PortfolioPage() {
  const { token } = useAuth();
  const [summary, setSummary] = useState<any>(null);
  const [symbol, setSymbol] = useState('AAPL');
  const [qty, setQty] = useState(1);

  const load = async () => token && setSummary(await apiGet('/portfolio/summary', token));
  useEffect(() => { load(); }, [token]);

  const trade = async (side: 'buy' | 'sell') => {
    if (!token) return;
    await apiPost('/portfolio/trade', { symbol, side, quantity: qty }, token);
    await load();
  };

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-semibold">Portfolio / Paper Trading</h2>
      <div className="grid md:grid-cols-3 gap-3">
        <div className="card">Total Value: ${summary?.total_value}</div>
        <div className="card">Cash: ${summary?.cash_balance}</div>
        <div className="card">Buying Power: ${summary?.buying_power}</div>
      </div>
      <div className="card flex gap-2">
        <input className="card" value={symbol} onChange={(e) => setSymbol(e.target.value.toUpperCase())} />
        <input className="card" type="number" value={qty} onChange={(e) => setQty(Number(e.target.value))} />
        <button className="rounded bg-green-700 px-3" onClick={() => trade('buy')}>Buy</button>
        <button className="rounded bg-red-700 px-3" onClick={() => trade('sell')}>Sell</button>
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        <div className="card overflow-auto">
          <table className="w-full text-sm">
            <thead><tr><th>Symbol</th><th>Qty</th><th>Mkt Value</th><th>Unrealized</th></tr></thead>
            <tbody>
              {summary?.holdings?.map((h: any) => (
                <tr key={h.symbol}><td>{h.symbol}</td><td>{h.quantity}</td><td>${h.market_value}</td><td>{h.unrealized_pnl}</td></tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="card">
          <PieChart width={320} height={220}>
            <Pie dataKey="market_value" data={summary?.holdings || []} nameKey="symbol" cx="50%" cy="50%" outerRadius={80}>
              {(summary?.holdings || []).map((_: any, i: number) => <Cell key={i} fill={colors[i % colors.length]} />)}
            </Pie>
            <Tooltip />
          </PieChart>
        </div>
      </div>
    </div>
  );
}

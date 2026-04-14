import { useEffect, useState } from 'react';
import { apiGet } from '../services/api';

export function MarketPage() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    apiGet('/market/overview').then(setData).catch(() => setData({ snapshots: [], news: [] }));
  }, []);

  return (
    <section>
      <h2>Market Overview</h2>
      <p>Bloomberg-inspired snapshots, watchlist-ready symbols, and simplified updates.</p>
      <div className="grid">
        {data?.snapshots?.map((s: any) => (
          <article key={s.symbol} className="panel">
            <h3>{s.symbol}</h3>
            <p>${s.price}</p>
            <p>{s.change_pct}%</p>
            <small>{s.plain_english}</small>
          </article>
        ))}
      </div>
    </section>
  );
}

import { useEffect, useState } from 'react';
import { apiGet, apiPost } from '../services/api';

export function PortfolioPage() {
  const [holdings, setHoldings] = useState<any[]>([]);
  const [symbol, setSymbol] = useState('AAPL');
  const [qty, setQty] = useState(1);

  async function load() {
    const data = await apiGet('/portfolio/holdings');
    setHoldings(data);
  }

  useEffect(() => {
    load().catch(() => setHoldings([]));
  }, []);

  async function trade(side: 'buy' | 'sell') {
    await apiPost('/portfolio/trade', { symbol, side, quantity: qty });
    await load();
  }

  return (
    <section>
      <h2>Portfolio</h2>
      <p>Persistent paper trading with virtual cash, holdings, and history-ready engine.</p>
      <div className="row">
        <input value={symbol} onChange={(e) => setSymbol(e.target.value.toUpperCase())} />
        <input type="number" value={qty} onChange={(e) => setQty(Number(e.target.value))} min={1} />
        <button onClick={() => trade('buy')}>Buy</button>
        <button onClick={() => trade('sell')}>Sell</button>
      </div>
      <div className="grid">
        {holdings.map((h) => (
          <article key={h.symbol} className="panel">
            <h3>{h.symbol}</h3>
            <p>Shares: {h.quantity}</p>
            <p>Avg Cost: ${h.avg_cost.toFixed(2)}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

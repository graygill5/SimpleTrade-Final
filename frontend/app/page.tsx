import Link from 'next/link';

export default function Landing() {
  return (
    <main className="min-h-screen bg-slatebg text-white p-12">
      <section className="max-w-5xl mx-auto">
        <h1 className="text-5xl font-bold mb-4">SimpleTrade</h1>
        <p className="text-slate-300 mb-8">Learn markets, paper trade, and grow with an AI market coach.</p>
        <div className="flex gap-3 mb-12">
          <Link href="/auth/signup" className="rounded bg-accent text-black font-semibold px-4 py-2">Sign Up</Link>
          <Link href="/auth/login" className="rounded border border-borderc px-4 py-2">Log In</Link>
        </div>
        <div className="grid md:grid-cols-2 gap-4">
          {['Market Overview', 'Community Chat', 'Portfolio Simulator', 'Learning Modules'].map((item) => (
            <div className="card" key={item}>
              <h3 className="font-semibold mb-2">{item}</h3>
              <p className="text-slate-400 text-sm">MVP module ready for local testing and iteration.</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}

import { Link, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { AiWidget } from './AiWidget';

export function AppLayout() {
  const { logout } = useAuth();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h1>SimpleTrade</h1>
        <nav>
          <Link to="/market">Market Overview</Link>
          <Link to="/chat">Community Chat</Link>
          <Link to="/portfolio">Portfolio</Link>
          <Link to="/learning">Learning Modules</Link>
        </nav>
        <button onClick={logout}>Logout</button>
      </aside>
      <main className="content">
        <Outlet />
      </main>
      <AiWidget />
    </div>
  );
}

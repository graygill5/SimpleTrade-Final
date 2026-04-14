import { Route, Routes } from 'react-router-dom';
import { AppLayout } from '../components/AppLayout';
import { ProtectedRoute } from '../components/ProtectedRoute';
import { ChatPage } from './ChatPage';
import { LearningPage } from './LearningPage';
import { LoginPage } from './LoginPage';
import { MarketPage } from './MarketPage';
import { PortfolioPage } from './PortfolioPage';

export function AppRouter() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route path="market" element={<MarketPage />} />
        <Route path="chat" element={<ChatPage />} />
        <Route path="portfolio" element={<PortfolioPage />} />
        <Route path="learning" element={<LearningPage />} />
      </Route>
    </Routes>
  );
}

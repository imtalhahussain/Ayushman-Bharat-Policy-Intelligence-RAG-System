import React, { useState, useEffect } from 'react';
import AuthPage from './pages/AuthPage';
import ChatPage from './pages/ChatPage';
import { Loader2 } from 'lucide-react';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [checkingAuth, setCheckingAuth] = useState(true);

  useEffect(() => {
    // Check if token exists
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
    setCheckingAuth(false);
  }, []);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  if (checkingAuth) {
    return (
      <div className="flex h-screen w-full items-center justify-center bg-slate-900 text-blue-500">
        <Loader2 className="animate-spin w-10 h-10" />
      </div>
    );
  }

  return (
    <>
      {isAuthenticated ? (
        <ChatPage onLogout={handleLogout} />
      ) : (
        <AuthPage onLogin={handleLogin} />
      )}
    </>
  );
}

export default App;

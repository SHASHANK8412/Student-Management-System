import { createContext, useContext, useEffect, useMemo, useState } from 'react';
import type { AuthResponse, AuthUser } from '@/types';
import * as authApi from '@/api/auth';

interface AuthContextValue {
  user: AuthUser | null;
  isAuthenticated: boolean;
  login: (payload: AuthResponse) => void;
  signOut: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('sfms_access_token');
    if (!token) {
      setLoading(false);
      return;
    }
    authApi.getCurrentUser()
      .then(setUser)
      .catch(() => {
        localStorage.removeItem('sfms_access_token');
        localStorage.removeItem('sfms_refresh_token');
      })
      .finally(() => setLoading(false));
  }, []);

  const value = useMemo<AuthContextValue>(() => ({
    user,
    isAuthenticated: Boolean(user),
    loading,
    login: (payload) => {
      localStorage.setItem('sfms_access_token', payload.tokens.access_token);
      localStorage.setItem('sfms_refresh_token', payload.tokens.refresh_token);
      setUser(payload.user);
    },
    signOut: () => {
      localStorage.removeItem('sfms_access_token');
      localStorage.removeItem('sfms_refresh_token');
      setUser(null);
    },
  }), [loading, user]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}

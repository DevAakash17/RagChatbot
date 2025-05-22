'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { apiService, LoginResponse } from './api';

interface AuthContextType {
  user: { id: string; username: string } | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  error: string | null;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<{ id: string; username: string } | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Check if user is already logged in
  useEffect(() => {
    const checkAuth = () => {
      try {
        const isAuth = apiService.isAuthenticated();
        if (!isAuth) {
          setUser(null);
          // Don't redirect here, we'll handle that in the protected routes
        } else {
          // Get the user from localStorage
          const currentUser = apiService.getCurrentUser();
          if (currentUser) {
            setUser(currentUser);
          } else {
            // If we have is_authenticated but no user data, clear the auth state
            apiService.logout();
            setUser(null);
          }
        }
      } catch (err) {
        console.error('Auth check error:', err);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (username: string, password: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await apiService.login(username, password);
      setUser(response); // The response now directly contains id and username
      router.push('/'); // Redirect to home/chat page after login
    } catch (err: any) {
      console.error('Login error:', err);
      setError(err.response?.data?.detail || 'Failed to login. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    apiService.logout();
    setUser(null);
    router.push('/login');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
        error,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

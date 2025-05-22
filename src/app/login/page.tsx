'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { LoginForm } from '@/components/auth/login-form';
import { useAuth } from '@/lib/auth-context';

export default function LoginPage() {
  const { isAuthenticated, isLoading, logout } = useAuth();
  const router = useRouter();

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated && !isLoading) {
      router.push('/');
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">Loading...</div>
      </div>
    );
  }

  if (isAuthenticated) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50">
        <div className="w-full max-w-md p-6 space-y-6 bg-white rounded-lg shadow-md">
          <div className="text-center">
            <h1 className="text-2xl font-bold">Already Logged In</h1>
            <p className="text-gray-600 mt-2">You are already logged in.</p>
          </div>
          <div className="flex flex-col space-y-4">
            <button
              onClick={() => router.push('/')}
              className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md"
            >
              Go to Chat
            </button>
            <button
              onClick={logout}
              className="w-full py-2 px-4 bg-red-600 hover:bg-red-700 text-white font-medium rounded-md"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50">
      <div className="w-full max-w-md">
        <LoginForm />
      </div>
    </div>
  );
}

'use client';

import { Chat } from '@/components/chat/chat';
import { ProtectedRoute } from '@/components/auth/protected-route';

export default function Home() {
  return (
    <ProtectedRoute>
      <main className="flex min-h-screen flex-col">
        <Chat />
      </main>
    </ProtectedRoute>
  );
}

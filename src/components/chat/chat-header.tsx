import React from 'react';
import { Button } from '@/components/ui/button';
import { RefreshCw } from 'lucide-react';
import { UserProfile } from '@/components/auth/user-profile';

interface ChatHeaderProps {
  onReset: () => void;
}

export function ChatHeader({ onReset }: ChatHeaderProps) {
  return (
    <div className="flex items-center justify-between p-4 border-b">
      <div className="flex items-center">
        <h1 className="text-xl font-bold">RAG Chatbot</h1>
      </div>
      <div className="flex items-center gap-4">
        <Button variant="outline" size="sm" onClick={onReset}>
          <RefreshCw className="h-4 w-4 mr-2" />
          Reset Chat
        </Button>
        <UserProfile />
      </div>
    </div>
  );
}

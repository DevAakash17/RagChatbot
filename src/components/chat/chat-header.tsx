import React from 'react';
import { Button } from '@/components/ui/button';
import { RefreshCw } from 'lucide-react';

interface ChatHeaderProps {
  onReset: () => void;
}

export function ChatHeader({ onReset }: ChatHeaderProps) {
  return (
    <div className="flex items-center justify-between p-4 border-b">
      <h1 className="text-xl font-bold">RAG Chatbot</h1>
      <Button variant="outline" size="sm" onClick={onReset}>
        <RefreshCw className="h-4 w-4 mr-2" />
        Reset Chat
      </Button>
    </div>
  );
}

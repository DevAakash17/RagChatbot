'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Message as MessageType } from '@/lib/types';
import { apiService } from '@/lib/api';
import { Message } from './message';
import { ChatInput } from './chat-input';
import { ChatHeader } from './chat-header';

export function Chat() {
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to the bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return;

    // Create a new user message
    const userMessage: MessageType = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

    // Add the user message to the chat
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Get previous user queries (up to 4)
      const prevQueries = messages
        .filter(msg => msg.role === 'user')
        .map(msg => msg.content)
        .slice(-4);

      // Send the query to the API with previous queries
      const response = await apiService.sendQuery(content, 'insurance_documents', prevQueries);

      // Create a new bot message
      const botMessage: MessageType = {
        id: (Date.now() + 1).toString(),
        role: 'bot',
        content: response.text,
        timestamp: new Date(),
      };

      // Add the bot message to the chat
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      console.error('Error sending message:', err);
      setError('Failed to send message. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setMessages([]);
    setError(null);
  };

  return (
    <div className="flex flex-col h-screen">
      <ChatHeader onReset={handleReset} />

      <div className="flex-1 overflow-y-auto p-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <p className="text-muted-foreground">
              Start a conversation by typing a message below.
            </p>
          </div>
        ) : (
          messages.map((message) => (
            <Message key={message.id} message={message} />
          ))
        )}

        {isLoading && (
          <div className="flex items-center justify-start gap-2 py-2">
            <div className="rounded-lg bg-muted px-4 py-2 max-w-[80%]">
              <div className="flex space-x-2">
                <div className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce" />
                <div className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce delay-75" />
                <div className="h-2 w-2 rounded-full bg-muted-foreground animate-bounce delay-150" />
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="flex items-center justify-center my-4">
            <p className="text-sm text-destructive">{error}</p>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
}

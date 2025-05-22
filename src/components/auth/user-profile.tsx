'use client';

import { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/lib/auth-context';
import { Button } from '@/components/ui/button';
import { LogOut, User } from 'lucide-react';

export function UserProfile() {
  const { user, logout } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const buttonRef = useRef<HTMLButtonElement>(null);

  // Handle click outside to close the menu
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        menuRef.current &&
        buttonRef.current &&
        !menuRef.current.contains(event.target as Node) &&
        !buttonRef.current.contains(event.target as Node)
      ) {
        setIsMenuOpen(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  if (!user) {
    return null;
  }

  return (
    <div className="relative">
      <Button
        ref={buttonRef}
        variant="ghost"
        size="sm"
        className="flex items-center gap-2"
        onClick={() => setIsMenuOpen(!isMenuOpen)}
      >
        <User className="h-4 w-4" />
        <span>{user.username}</span>
      </Button>

      {isMenuOpen && (
        <div
          ref={menuRef}
          className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10 border"
        >
          <div className="px-4 py-2 text-sm text-gray-700 border-b">
            <div className="font-medium">Signed in as</div>
            <div className="truncate">{user.username}</div>
          </div>
          <button
            onClick={() => {
              logout();
              setIsMenuOpen(false);
            }}
            className="flex w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
          >
            <LogOut className="h-4 w-4 mr-2" />
            Sign out
          </button>
        </div>
      )}
    </div>
  );
}

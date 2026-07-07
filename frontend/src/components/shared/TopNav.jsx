import React from 'react';
import { Bell, Menu, Search, User } from 'lucide-react';

export function TopNav() {
  return (
    <header className="h-16 border-b border-border bg-background/80 backdrop-blur-md sticky top-0 z-10 flex items-center justify-between px-4 lg:px-8">
      <div className="flex items-center gap-4">
        <button className="md:hidden text-muted hover:text-primary">
          <Menu className="w-5 h-5" />
        </button>
        <div className="hidden md:flex items-center gap-2 text-muted bg-surface border border-border rounded-md px-3 py-1.5 w-64 focus-within:border-accent focus-within:ring-1 focus-within:ring-accent transition-all">
          <Search className="w-4 h-4" />
          <input 
            type="text" 
            placeholder="Search forecasts..." 
            className="bg-transparent border-none outline-none text-sm w-full text-primary placeholder-muted"
          />
        </div>
      </div>

      <div className="flex items-center gap-4">
        <button className="text-muted hover:text-primary transition-colors relative">
          <Bell className="w-5 h-5" />
          <span className="absolute top-0 right-0 w-2 h-2 bg-accent rounded-full border border-background"></span>
        </button>
        <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-accent to-purple-500 p-0.5 cursor-pointer">
          <div className="w-full h-full rounded-full bg-surface flex items-center justify-center">
            <User className="w-4 h-4 text-primary" />
          </div>
        </div>
      </div>
    </header>
  );
}

import React from 'react';
import { Sidebar } from '../components/shared/Sidebar';
import { TopNav } from '../components/shared/TopNav';

export function DashboardLayout({ children, activeTab, setActiveTab }) {
  return (
    <div className="min-h-screen bg-background flex">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="flex-1 md:ml-64 flex flex-col min-w-0">
        <TopNav />
        <main className="flex-1 p-4 md:p-8 overflow-y-auto">
          <div className="max-w-6xl mx-auto pb-20">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
}

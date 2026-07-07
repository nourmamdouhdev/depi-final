import React from 'react';
import { LayoutDashboard, UploadCloud, TrendingUp, Settings, PieChart, FileText } from 'lucide-react';

export function Sidebar({ activeTab, setActiveTab }) {
  const menuItems = [
    { id: 'dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { id: 'upload', icon: UploadCloud, label: 'Upload Dataset' },
    { id: 'forecast', icon: TrendingUp, label: 'Forecast Results' },
    { id: 'analytics', icon: PieChart, label: 'Analytics' },
    { id: 'export', icon: FileText, label: 'Export Reports' },
  ];

  const handleNavClick = (id) => {
    if (setActiveTab) setActiveTab(id);
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 border-r border-border bg-background hidden md:flex flex-col z-10">
      <div className="h-16 flex items-center px-6 border-b border-border">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded bg-primary flex items-center justify-center">
            <TrendingUp className="w-4 h-4 text-background" strokeWidth={3} />
          </div>
          <span className="font-semibold text-primary tracking-tight">Forecast AI</span>
        </div>
      </div>
      
      <div className="flex-1 overflow-y-auto py-6 px-3">
        <div className="text-xs font-medium text-muted uppercase tracking-wider mb-3 px-3">
          Overview
        </div>
        <nav className="space-y-1">
          {menuItems.map((item) => (
            <button 
              key={item.id}
              onClick={() => handleNavClick(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors ${
                activeTab === item.id 
                  ? 'bg-white/10 text-primary font-medium' 
                  : 'text-muted hover:text-primary hover:bg-white/5'
              }`}
            >
              <item.icon className="w-4 h-4" />
              {item.label}
            </button>
          ))}
        </nav>
      </div>

      <div className="p-4 border-t border-border">
        <button className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-muted hover:text-primary hover:bg-white/5 transition-colors">
          <Settings className="w-4 h-4" />
          Settings
        </button>
      </div>
    </aside>
  );
}

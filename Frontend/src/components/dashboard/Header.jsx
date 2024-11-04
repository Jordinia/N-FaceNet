import React from 'react';
import { Bell } from 'lucide-react';

export const Header = () => {
  return (
    <header className="flex items-center justify-between mb-8">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <div className="flex items-center gap-4">
        <button className="p-2 hover:bg-gray-100 rounded-full">
          <Bell className="w-6 h-6" />
        </button>
        <div className="flex items-center gap-3">
          <img
            src="/api/placeholder/40/40"
            alt="Profile"
            className="w-10 h-10 rounded-full"
          />
          <div>
            <div className="font-semibold">Christopher</div>
            <div className="text-sm text-gray-500">Admin</div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
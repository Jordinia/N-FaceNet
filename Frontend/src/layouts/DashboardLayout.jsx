// src/layouts/DashboardLayout.jsx
import React from 'react';
import Header from '../components/dashboard/Header';

const DashboardLayout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="flex flex-col h-screen">
        {/* Sidebar - if needed */}
        <div className="flex-grow flex">
          <main className="flex-1 overflow-auto">
            <div className="p-8">
              <Header />
              {children}
            </div>
          </main>
        </div>
      </div>
    </div>
  );
};

export default DashboardLayout;
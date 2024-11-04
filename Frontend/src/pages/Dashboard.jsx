import React from 'react';
import { Header } from '../components/dashboard/Header';
import { RoomsList } from '../components/dashboard/RoomsList';
import { EmployeesList } from '../components/dashboard/EmployeesList';
import { WarningPanel } from '../components/dashboard/WarningPanel';

const Dashboard = () => {
  const rooms = [
    {
      id: 1,
      name: 'Meeting Room',
      image: '/api/placeholder/400/300',
      capacity: '3/10'
    },
    {
      id: 2,
      name: 'Gym Room',
      image: '/api/placeholder/400/300',
      capacity: '15/20'
    }
  ];

  const employees = [
    {
      id: 1,
      name: 'Christopher',
      role: 'Developer',
      location: 'Server Room',
      avatar: '/api/placeholder/40/40'
    },
    {
      id: 2,
      name: 'Christopher',
      role: 'Section Head',
      location: 'Server Room',
      avatar: '/api/placeholder/40/40'
    },
    {
      id: 3,
      name: 'Christopher',
      role: 'Section Head',
      location: 'Server Room',
      avatar: '/api/placeholder/40/40'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <Header />
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <RoomsList rooms={rooms} />
        <div className="space-y-8">
          <WarningPanel />
          <EmployeesList employees={employees} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
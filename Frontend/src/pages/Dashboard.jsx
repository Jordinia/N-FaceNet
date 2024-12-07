import React from 'react';
import { Header } from '../components/dashboard/Header';
import { RoomsList } from '../components/dashboard/RoomsList';
import { EmployeesList } from '../components/dashboard/EmployeesList';
import { WarningPanel } from '../components/dashboard/WarningPanel';

// Dummy Data
import { rooms } from '../utils/dummy/roomData';

const Dashboard = () => {
  const handleAddRoom = ({ name, capacity }) => {
    const newRoom = {
      id: Date.now(),
      name,
      image: 'http://fakeimg.pl/400x300',
      capacity
    }
    
    rooms.push(newRoom)
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <Header />
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <RoomsList rooms={rooms} handleAddRoom={handleAddRoom} />
        <div className="space-y-8">
          <WarningPanel />
          <EmployeesList />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
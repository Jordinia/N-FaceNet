import React from 'react';
import { Plus } from 'lucide-react';
import { RoomCard } from './RoomCard';

export const RoomsList = ({ rooms }) => {
  return (
    <div className="lg:col-span-2">
      <h2 className="text-xl font-bold mb-4">Rooms</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {rooms.map(room => (
          <RoomCard key={room.id} room={room} />
        ))}
        <button className="flex items-center justify-center h-48 rounded-xl bg-gray-100 hover:bg-gray-200 transition-colors">
          <div className="flex flex-col items-center gap-2">
            <Plus className="w-8 h-8" />
            <span className="font-medium">Add Room</span>
          </div>
        </button>
      </div>
    </div>
  );
};

export default RoomsList;
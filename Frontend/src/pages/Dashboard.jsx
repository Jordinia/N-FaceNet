import React, { useState, useEffect } from 'react';
import { Header } from '../components/dashboard/Header';
import { RoomsList } from '../components/dashboard/RoomsList';
import { EmployeesList } from '../components/dashboard/EmployeesList';
import { TokenList } from '../components/dashboard/TokenList';
import { WarningPanel } from '../components/dashboard/WarningPanel';

const Dashboard = () => {
  const [rooms, setRooms] = useState([]);

  // Fetch rooms initially
  useEffect(() => {
    const fetchRooms = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/room');
        if (!response.ok) {
          throw new Error(`Failed to fetch rooms: ${response.statusText}`);
        }
        const data = await response.json();
        if (data.status === 'success') {
          const formattedRooms = data.data.map(room => ({
            room_id: room.room_id,
            room: room.room,
            capacity: room.capacity,
            image: `https://placehold.co/400x400?text=${encodeURIComponent(room.room)}`,
          }));
          setRooms(formattedRooms);
        }
      } catch (error) {
        console.error('Error fetching rooms:', error);
      }
    };

    fetchRooms();
  }, []);

  const handleAddRoom = async ({ room, capacity }) => {
    const newRoom = { room, capacity };

    try {
      const response = await fetch('http://127.0.0.1:5000/room', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newRoom),
      });

      if (!response.ok) {
        throw new Error(`Failed to add room: ${response.statusText}`);
      }

      const result = await response.json();
      console.log('Room added successfully:', result);

      // Add the new room to the rooms list
      setRooms(prevRooms => [
        ...prevRooms,
        {
          room_id: result.data.room_id,
          room: result.data.room,
          capacity: result.data.capacity,
          image: `https://placehold.co/400x400?text=${encodeURIComponent(result.data.room)}`,
        },
      ]);
    } catch (error) {
      console.error('Error adding room:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <Header />
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <RoomsList rooms={rooms} handleAddRoom={handleAddRoom} />
        <div className="space-y-8">
          <WarningPanel />
          <EmployeesList />
          <TokenList />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

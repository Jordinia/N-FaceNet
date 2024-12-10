import React, { useEffect, useState } from 'react';
import { Plus } from 'lucide-react';
import { RoomCard } from './RoomCard';
import { Modal } from 'antd';

export const RoomsList = ({ rooms, handleAddRoom }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [room, setRoom] = useState('');
  const [capacity, setCapacity] = useState(0);
  const [roomData, setRoomData] = useState([]); // To store room data with currentPeople

  // Fetch current people count for each room
  const fetchRoomPeopleCount = async (roomId) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/employee?current_room_id=${roomId}`);
      const data = await response.json();
      
      // Return the count (number of people) in the room
      return data.count;
    } catch (error) {
      console.error('Error fetching room data:', error);
      return 0; // Return 0 in case of an error
    }
  };

  useEffect(() => {
    // Fetch currentPeople for each room
    const fetchData = async () => {
      const roomsWithPeople = await Promise.all(
        rooms.map(async (room) => {
          const currentPeople = await fetchRoomPeopleCount(room.room_id);
          return { ...room, currentPeople }; // Add currentPeople to each room
        })
      );
      setRoomData(roomsWithPeople); // Update the state with rooms data including currentPeople
    };

    fetchData();
  }, [rooms]); // Re-fetch when rooms change

  const showModal = () => {
    setIsModalOpen(true);
  };

  const handleOk = async () => {
    if (!room || !capacity) return;

    await handleAddRoom({ room, capacity });

    // Reset modal state
    setIsModalOpen(false);
    setRoom('');
    setCapacity(0);
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  return (
    <div className="lg:col-span-2">
      <h2 className="text-xl font-bold mb-4">Rooms</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {roomData.map(room => (
          <RoomCard key={room.room_id} room={room} />
        ))}
        <button
          onClick={showModal}
          className="flex items-center justify-center h-48 rounded-xl bg-gray-100 hover:bg-gray-200 transition-colors"
        >
          <div className="flex flex-col items-center gap-2">
            <Plus className="w-8 h-8" />
            <span className="font-medium">Add Room</span>
          </div>
        </button>
      </div>

      {/* Modal */}
      <Modal title="Add Room" open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
        <div className="flex gap-2 w-full items-center justify-center">
          <div className="flex flex-col w-full">
            <label htmlFor="room">Room</label>
            <input
              value={room}
              onChange={(e) => setRoom(e.target.value)}
              id="room"
              type="text"
              className="w-full px-4 py-2 rounded-lg"
            />
          </div>
          <div className="flex flex-col w-full">
            <label htmlFor="capacity">Capacity</label>
            <input
              value={capacity}
              onChange={(e) => setCapacity(e.target.value)}
              id="capacity"
              type="number"
              className="w-full px-4 py-2 rounded-lg"
            />
          </div>
        </div>
      </Modal>
    </div>
  );
};

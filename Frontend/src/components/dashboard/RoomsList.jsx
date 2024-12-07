import React, { useState } from 'react';
import { Plus } from 'lucide-react';
import { RoomCard } from './RoomCard';

import { Modal } from 'antd';


export const RoomsList = ({ rooms, handleAddRoom }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [roomName, setRoomName] = useState("");
  const [roomCapacity, setRoomCapacity] = useState(0);

  const showModal = () => {
    setIsModalOpen(true);
  };

  const handleOk = () => {
    if (!roomName || !roomCapacity) return;

    setIsModalOpen(false);
    handleAddRoom({
      id: Date.now(),
      name: roomName,
      image: 'http://fakeimg.pl/400x300',
      capacity: roomCapacity
    })
    setRoomName("");
    setRoomCapacity(0);
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  return (
    <div className="lg:col-span-2">
      <h2 className="text-xl font-bold mb-4">Rooms</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {rooms.map(room => (
          <RoomCard key={room.id} room={room} />
        ))}
        <button onClick={showModal} className="flex items-center justify-center h-48 rounded-xl bg-gray-100 hover:bg-gray-200 transition-colors">
          <div className="flex flex-col items-center gap-2">
            <Plus className="w-8 h-8" />
            <span className="font-medium">Add Room</span>
          </div>
        </button>
      </div>

      {/* Modal */}
      <Modal title="Add Room" open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
        <div className='flex gap-2 w-full items-center justify-center'>
          <div className='flex flex-col w-full'>
            <label htmlFor="room_name">Room Name</label>
            <input value={roomName} onChange={(e) => setRoomName(e.target.value)} id='room_name' type="text" className='w-full px-4 py-2 rounded-lg' />

          </div>
          <div className='flex flex-col w-full'>
            <label htmlFor="capacity">Room Capacity</label>
            <input value={roomCapacity} onChange={(e) => setRoomCapacity(e.target.value)} id='capacity' type="number" className='w-full px-4 py-2 rounded-lg' />
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default RoomsList;
import React from 'react';
import { Link } from 'react-router-dom';

export const RoomCard = ({ room }) => {
  return (
    <Link to={`/room/${room.id}`} className="block">
      <div className="relative rounded-xl overflow-hidden transition-transform hover:scale-105">
        <img
          src={'/images/rooms/' + room.image}
          alt={room.name}
          className="w-full h-48 object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
        <div className="absolute top-4 left-4 bg-white/90 rounded-full px-3 py-1 text-sm">
          <span className="flex items-center gap-1">0/{room.capacity}</span>
        </div>
        <div className="absolute bottom-4 left-4 text-white">
          <h3 className="text-xl font-bold">{room.name}</h3>
        </div>
      </div>
    </Link>
  );
};

export default RoomCard;
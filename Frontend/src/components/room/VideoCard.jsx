// src/components/room/VideoCard.js
import React from 'react';

const VideoCard = ({ streamUrl }) => {
  return (
    <div className="video-card">
      <h2>Live Video Stream</h2>
      <div className="aspect-video bg-gray-100 rounded-lg mb-4 overflow-hidden">
        {/* Camera feed */}
        <img
          src={streamUrl}
          alt="MJPEG Stream"
          className="w-full h-full object-cover"
          loading="eager"
        />
      </div>
    </div>
  );
};

export default VideoCard;

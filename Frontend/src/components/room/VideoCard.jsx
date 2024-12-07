// src/components/room/VideoCard.js
import React from 'react';

const VideoCard = ({ streamUrl }) => {
  return (
    <div className="video-card">
      <h2>Live Video Stream</h2>
      <div className="video-container">
        <iframe id="videoFrame" src={streamUrl} width="640" height="480"></iframe>
      </div>
    </div>
  );
};

export default VideoCard;

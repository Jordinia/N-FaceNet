// src/VideoPage.js
import React from 'react';
import VideoCard from '../components/room/VideoCard';

const VideoPage = () => {

    return (
        <div className="video-page">
            <h1>Video Streaming Page</h1>
            <VideoCard streamUrl={droidCamUrl} />
        </div>
    );
};

export default VideoPage;

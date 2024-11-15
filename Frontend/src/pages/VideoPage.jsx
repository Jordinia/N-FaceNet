// src/VideoPage.js
import React from 'react';
import VideoCard from '../components/room/VideoCard';

const VideoPage = () => {
    // Replace with your DroidCam IP and port
    const droidCamUrl = 'http://10.10.0.214:65000/video';

    return (
        <div className="video-page">
            <h1>Video Streaming Page</h1>
            <VideoCard streamUrl={droidCamUrl} />
        </div>
    );
};

export default VideoPage;

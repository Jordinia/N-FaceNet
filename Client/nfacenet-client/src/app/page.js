'use client'

import React, { useRef, useEffect, useState } from "react";

export default function Home() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [photo, setPhoto] = useState(null);

  useEffect(() => {
    // Access user's webcam
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
          }
        })
        .catch((err) => console.error("Error accessing webcam: ", err));
    }
  }, []);

  const handleCapturePhoto = () => {
    if (videoRef.current && canvasRef.current) {
      const canvas = canvasRef.current;
      const context = canvas.getContext("2d");
      const video = videoRef.current;

      // Set canvas dimensions to match the video
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      // Draw the current video frame to the canvas
      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      // Get the image data URL
      const photoData = canvas.toDataURL("image/png");
      setPhoto(photoData);

      console.log("Photo captured:", photoData);
    }
  };

  const handleInputKeyDown = (event) => {
    if (event.key === "Enter") {
      handleCapturePhoto();
    }
  };

  const handleRegister = () => {
    alert("Register button clicked!");
    // Registration logic can be added here
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      {/* Webcam View */}
      <div className="relative w-full max-w-3xl aspect-video border-4 border-gray-300 rounded-lg overflow-hidden shadow-md">
        <video
          ref={videoRef}
          className="w-full h-full object-cover"
          autoPlay
          muted
        ></video>
      </div>

      {/* Registration Button */}
      <button
        onClick={handleRegister}
        className="mt-8 px-6 py-3 bg-green-600 text-white rounded-full shadow-lg hover:bg-green-500 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2"
      >
        Register
      </button>

      {/* Input Field for Photo Capture */}
      <input
        type="text"
        placeholder="Press Enter to capture"
        onKeyDown={handleInputKeyDown}
        className="mt-4 px-6 py-3 w-64 text-center bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
      />

      {/* Canvas (hidden for photo capture) */}
      <canvas ref={canvasRef} className="hidden"></canvas>

      {/* Display Captured Photo */}
      {photo && (
        <img
          src={photo}
          alt="Captured"
          className="mt-8 w-64 h-auto rounded-lg border-2 border-gray-300"
        />
      )}
    </div>
  );
}

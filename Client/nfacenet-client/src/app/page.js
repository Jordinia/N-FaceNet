'use client'

import React, { useRef, useEffect, useState } from "react";
import { useRouter } from 'next/navigation'; // Import the useRouter hook

export default function Home() {
  const videoRef1 = useRef(null);
  const videoRef2 = useRef(null);
  const canvasRef1 = useRef(null);
  const canvasRef2 = useRef(null);
  const inputRef = useRef(null); // Ref for the input field
  const [photo1, setPhoto1] = useState(null);
  const [photo2, setPhoto2] = useState(null);
  const [photoIndex, setPhotoIndex] = useState(1); // Counter for Body Camera photos
  const [employeeNik, setemployeeNik] = useState(""); // State to store input text
  const [deviceIds, setDeviceIds] = useState({ faceCamera: null, bodyCamera: null });
  
  const router = useRouter(); // Initialize the useRouter hook

  useEffect(() => {
    // Autofocus the input field when the component mounts
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  // Function moved out of useEffect
  const getVideoStream = async (deviceId, videoRef) => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { deviceId: { exact: deviceId } }
      });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      console.error("Error accessing webcam: ", err);
    }
  };

  useEffect(() => {
    const getCameras = async () => {
      const devices = await navigator.mediaDevices.enumerateDevices();
      const videoDevices = devices.filter(device => device.kind === "videoinput");

      if (videoDevices.length >= 2) {
        setDeviceIds({
          faceCamera: videoDevices[0].deviceId,
          bodyCamera: videoDevices[1].deviceId
        });
        getVideoStream(videoDevices[0].deviceId, videoRef1);
        getVideoStream(videoDevices[1].deviceId, videoRef2);
      } else {
        console.error("Not enough cameras found");
      }
    };

    getCameras();
  }, []);

  const handleFlipCameras = () => {
    setDeviceIds(prev => ({
      faceCamera: prev.bodyCamera,
      bodyCamera: prev.faceCamera
    }));

    // Swap the video streams
    getVideoStream(deviceIds.bodyCamera, videoRef1);
    getVideoStream(deviceIds.faceCamera, videoRef2);
  };

  const handleCapturePhotos = () => {
    if (!employeeNik) {
      alert("Please enter an employee ID before capturing photos.");
      return;
    }

    // Capture photo from Face Camera
    if (videoRef1.current && canvasRef1.current) {
      const canvas = canvasRef1.current;
      const context = canvas.getContext("2d");
      const video = videoRef1.current;

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      const photoData1 = canvas.toDataURL("image/png");
      setPhoto1(`F_${photoData1}`); // Prefix with F
      sendImageToBackend(photoData1, "F", employeeNik);
    }

    // Capture photo from Body Camera
    if (videoRef2.current && canvasRef2.current) {
      const canvas = canvasRef2.current;
      const context = canvas.getContext("2d");
      const video = videoRef2.current;

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      const photoData2 = canvas.toDataURL("image/png");
      setPhoto2(`B_${photoIndex}_${photoData2}`); // Prefix with B and index
      sendImageToBackend(photoData2, `B`, employeeNik);
      setPhotoIndex(photoIndex + 1); // Increment the index
    }
  };

  const sendImageToBackend = async (imageData, prefix, employeeNik) => {
    try {
        console.log({ image: imageData, prefix, employee_nik: employeeNik });

        const response = await fetch("/api/checkin-image", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ image: imageData, prefix, employee_nik: employeeNik }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log("Image saved successfully:", result);

        // Refresh the page on success
        window.location.reload();
    } catch (error) {
        console.error("Error sending image to backend:", error);
    }
};

  const handleInputKeyDown = (event) => {
    if (event.key === "Enter") {
      handleCapturePhotos();
    }
  };

  // New function to navigate to the register page
  const handleGoToRegister = () => {
    router.push('/register'); // Navigate to /register page
  };

  const handleGoToSignUp = () => {
    router.push('/signup'); // Navigate to /register page
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      {/* Two Video Frames */}
      <div className="flex space-x-8">
        <div className="flex flex-col items-center">
          <label className="text-lg font-semibold mb-2">Face Camera</label>
          <div className="relative w-full max-w-md aspect-video border-4 border-gray-300 rounded-lg overflow-hidden shadow-md">
            <video
              ref={videoRef1}
              className="w-full h-full object-cover"
              autoPlay
              muted
            ></video>
          </div>
        </div>
        <div className="flex flex-col items-center">
          <label className="text-lg font-semibold mb-2">Body Camera</label>
          <div className="relative w-full max-w-md aspect-video border-4 border-gray-300 rounded-lg overflow-hidden shadow-md">
            <video
              ref={videoRef2}
              className="w-full h-full object-cover"
              autoPlay
              muted
            ></video>
          </div>
        </div>
      </div>

      {/* Flip Cameras Button */}
      <button
        onClick={handleFlipCameras}
        className="mt-6 p-2 bg-gray-300 rounded-full shadow-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2"
      >
        Flip Cameras
      </button>

      {/* Input Field for Photo Capture */}
      <input
        ref={inputRef}
        type="text"
        placeholder="Enter Employee ID and Press Enter"
        value={employeeNik}
        onChange={(e) => setemployeeNik(e.target.value)}
        onKeyDown={handleInputKeyDown}
        className="mt-8 px-6 py-3 w-64 text-center bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
      />

      {/* Canvas (hidden for photo capture) */}
      <div className="flex flex-row space-x-4">
        <canvas ref={canvasRef1} className="hidden"></canvas>
        <canvas ref={canvasRef2} className="hidden"></canvas>
      </div>

      {/* Display Captured Photos */}
      <div className="flex flex-row space-x-4">
        {photo1 && (
          <div className="mt-8 flex flex-col items-center">
            <label className="text-lg font-semibold mb-2">Captured Photo from Face Camera</label>
            <img
              src={photo1.split('_')[1]} // Remove the prefix for the src
              alt="Captured from Face Camera"
              className="w-64 h-auto rounded-lg border-2 border-gray-300"
            />
          </div>
        )}
        {photo2 && (
          <div className="mt-8 flex flex-col items-center">
            <label className="text-lg font-semibold mb-2">Captured Photo from Body Camera</label>
            <img
              src={photo2.split('_')[2]} // Remove the prefix for the src
              alt="Captured from Body Camera"
              className="w-64 h-auto rounded-lg border-2 border-gray-300"
            />
          </div>
        )}
      </div>

      {/* New Button to Go to Register Page */}
      <div className="flex flex-row space-x-4">
        <button
          onClick={handleGoToRegister}
          className="mt-6 p-2 bg-green-500 text-white rounded-full shadow-md hover:bg-green-400 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2"
        >
          Register
        </button>
        
        {/* New Button to Go to Register Page */}
        <button
          onClick={handleGoToSignUp}
          className="mt-6 p-2 bg-green-500 text-white rounded-full shadow-md hover:bg-green-400 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2"
        >
          Sign Up
        </button>
      </div>
    </div>
  );
}

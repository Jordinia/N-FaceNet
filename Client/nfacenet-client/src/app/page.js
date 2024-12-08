'use client'

import React, { useRef, useEffect, useState } from "react";

export default function Home() {
  const videoRef1 = useRef(null);
  const videoRef2 = useRef(null);
  const canvasRef1 = useRef(null);
  const canvasRef2 = useRef(null);
  const [photo1, setPhoto1] = useState(null);
  const [photo2, setPhoto2] = useState(null);
  const [photoIndex, setPhotoIndex] = useState(1); // Counter for Body Camera photos
  const [employeeNik, setemployeeNik] = useState(""); // State to store input text

  useEffect(() => {
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

    const getCameras = async () => {
      const devices = await navigator.mediaDevices.enumerateDevices();
      const videoDevices = devices.filter(device => device.kind === "videoinput");

      if (videoDevices.length >= 2) {
        getVideoStream(videoDevices[0].deviceId, videoRef1);
        getVideoStream(videoDevices[1].deviceId, videoRef2);
      } else {
        console.error("Not enough cameras found");
      }
    };

    getCameras();
  }, []);

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
      console.log({ image: imageData, prefix, employee_nik: employeeNik })

      const response = await fetch("/api/save-image", {
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
    } catch (error) {
      console.error("Error sending image to backend:", error);
    }
  };

  const handleInputKeyDown = (event) => {
    if (event.key === "Enter") {
      handleCapturePhotos();
    }
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

      {/* Input Field for Photo Capture */}
      <input
        type="text"
        placeholder="Enter Employee ID and Press Enter"
        value={employeeNik}
        onChange={(e) => setemployeeNik(e.target.value)}
        onKeyDown={handleInputKeyDown}
        className="mt-8 px-6 py-3 w-64 text-center bg-blue-600 text-white rounded-full shadow-lg hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2"
      />

      {/* Canvas (hidden for photo capture) */}
      <canvas ref={canvasRef1} className="hidden"></canvas>
      <canvas ref={canvasRef2} className="hidden"></canvas>

      {/* Display Captured Photos */}
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
  );
}

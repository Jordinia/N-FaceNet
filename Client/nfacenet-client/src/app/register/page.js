'use client'

import React, { useRef, useEffect, useState } from "react";
import axios from "axios"; // Import axios for API request

export default function Registration() {
    const videoRef = useRef(null); // Reference for the camera frame
    const canvasRef = useRef(null); // Reference for the canvas to capture photos
    const [inputValue, setInputValue] = useState(""); // State for input field
    const [currentDeviceId, setCurrentDeviceId] = useState(null); // State to track the current camera device
    const [availableDevices, setAvailableDevices] = useState([]); // List of available video devices
    const [capturing, setCapturing] = useState(false); // State to prevent multiple triggers
    const [capturedImages, setCapturedImages] = useState([]); // State to store captured images
    const [countdown, setCountdown] = useState(null); // State for countdown timer
    const [employee_id, setEmployee_id] = useState(null); // State for employee ID after fetching from token
    const [token, setToken] = useState(null); // State for token

    // Initialize camera with a specific device ID
    const initializeCamera = async (deviceId) => {
        try {
            const constraints = deviceId
                ? { video: { deviceId: { exact: deviceId } } }
                : { video: true };

            const stream = await navigator.mediaDevices.getUserMedia(constraints);
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
            }
        } catch (err) {
            console.error("Error accessing webcam: ", err);
        }
    };

    // Get the list of available video devices
    const getAvailableDevices = async () => {
        const devices = await navigator.mediaDevices.enumerateDevices();
        const videoDevices = devices.filter((device) => device.kind === "videoinput");
        setAvailableDevices(videoDevices);
        if (videoDevices.length > 0) {
            setCurrentDeviceId(videoDevices[0].deviceId);
            initializeCamera(videoDevices[0].deviceId); // Initialize with the first device
        }
    };

    // Switch to the next camera
    const switchCamera = () => {
        if (availableDevices.length > 1) {
            const currentIndex = availableDevices.findIndex(
                (device) => device.deviceId === currentDeviceId
            );
            const nextIndex = (currentIndex + 1) % availableDevices.length;
            const nextDeviceId = availableDevices[nextIndex].deviceId;
            setCurrentDeviceId(nextDeviceId);
            initializeCamera(nextDeviceId);
        } else {
            alert("No other camera available to switch.");
        }
    };

    const capturePhoto = async (employee_id, token) => {
        if (videoRef.current && canvasRef.current) {
            const canvas = canvasRef.current;
            const context = canvas.getContext("2d");
            context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
            const dataURL = canvas.toDataURL("image/png");

            // Add the captured photo to the list of captured images
            setCapturedImages((prevImages) => [...prevImages, dataURL]);

            // Send the captured photo to the API with token and employee_id
            await sendPhotoToAPI(dataURL, employee_id, token);
        }
    };

    const sendPhotoToAPI = async (image, employee_id, token) => {
        if (!employee_id || !token) {
            console.error("Employee ID or Token is missing.");
            return;
        }

        try {
            const response = await axios.post("/api/register-image", {
                image: image,
                employee_id: employee_id,
                token: token,
            });

            console.log("API response: ", response.data);

            // Clear images after successful upload
            setCapturedImages((prevImages) => prevImages.filter((img) => img !== image));
        } catch (error) {
            console.error("Error sending image to API: ", error);
        }
    };

    const startPhotoCapture = async (employee_id, token) => {
        if (capturing) return; // Prevent multiple triggers
        setCapturing(true);
        let count = 3; // Set the number of photos to capture
        let photosCaptured = 0;

        const countdownInterval = setInterval(() => {
            setCountdown(count);
            if (count === 0) {
                capturePhoto(employee_id, token);
                photosCaptured++;
                count = 3; // Reset countdown after capture
                if (photosCaptured >= 3) {
                    clearInterval(countdownInterval);
                    setCapturing(false);
                    setCountdown(null); // Clear countdown after all photos are captured
                }
            } else {
                count--;
            }
        }, 1000);
    };

    useEffect(() => {
        getAvailableDevices(); // Fetch available devices on component mount
    }, []);

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };

    const handleKeyDown = async (e) => {
        if (e.key === "Enter" && inputValue.trim() !== "") {
            try {
                const tokenResponse = await axios.get(`http://localhost:5000/token/${inputValue}`);
                const tokenData = tokenResponse.data.data;

                if (tokenData && tokenData.employee_id) {
                    setEmployee_id(tokenData.employee_id);
                    setToken(tokenData.token);
                    startPhotoCapture(tokenData.employee_id, tokenData.token);
                } else {
                    alert("Invalid token or employee ID not found.");
                }
            } catch (error) {
                console.error("Error fetching employee data:", error);
                alert("Error fetching employee data.");
            }
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            {/* Camera Frame */}
            <div className="flex flex-col items-center">
                <label className="text-lg font-semibold mb-2">Camera</label>
                <div className="relative w-full max-w-md aspect-video border-4 border-gray-300 rounded-lg overflow-hidden shadow-md">
                    <video
                        ref={videoRef}
                        className="w-full h-full object-cover"
                        autoPlay
                        muted
                    ></video>
                </div>
            </div>

            {/* Hidden Canvas for Capturing Photos */}
            <canvas
                ref={canvasRef}
                className="hidden"
                width={640}
                height={480}
            ></canvas>

            {/* Captured Images */}
            <div className="mt-4 flex gap-2 flex-wrap">
                {capturedImages.map((image, index) => (
                    <img
                        key={index}
                        src={image}
                        alt={`Captured ${index + 1}`}
                        className="w-32 h-32 object-cover border border-gray-300 rounded-lg"
                    />
                ))}
            </div>

            {/* Countdown Timer */}
            {countdown !== null && (
                <div className="text-2xl font-bold text-red-600 mt-4">
                    {`Capture in: ${countdown}s`}
                </div>
            )}

            {/* Switch Camera Button */}
            <button
                onClick={switchCamera}
                className="mt-4 px-6 py-3 bg-green-600 text-white rounded-full shadow-lg hover:bg-green-500 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-2"
            >
                Switch Camera
            </button>

            {/* Input Field */}
            <input
                type="text"
                placeholder="Enter your details (e.g. NIK)"
                value={inputValue}
                onChange={handleInputChange}
                onKeyDown={handleKeyDown}
                className="mt-8 px-6 py-3 w-64 text-center bg-blue-600 text-white rounded-lg"
            />
        </div>
    );
}

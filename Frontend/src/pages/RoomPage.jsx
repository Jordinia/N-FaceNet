import React, { useState, useEffect, useRef } from 'react';
import { ArrowLeft, Plus, Trash2 } from 'lucide-react';
import { Link, useParams } from 'react-router-dom';
import axios from 'axios';

const RoomPage = () => {
  const [streamUrl, setStreamUrl] = useState(null); // Dynamically set from API
  const videoRef = useRef(null); // Ref for the video element
  const [cameras, setCameras] = useState([]);
  const [showAddCamera, setShowAddCamera] = useState(false);
  const [newCamera, setNewCamera] = useState({ name: '', url: '' });
  const [detectedUsers, setDetectedUsers] = useState([]);
  const { id } = useParams(); // Room ID from URL params

  const rooms = [
    { id: 1, name: 'Common Room' },
    { id: 2, name: 'Bedroom' },
    { id: 3, name: 'Kitchen' },
  ];
  const room = rooms.find((r) => r.id === parseInt(id));

  useEffect(() => {
    // Fetch camera data for the room
    const fetchCameraData = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/camera/room/${id}`);
        if (response.data && response.data.data.length > 0) {
          const cameraData = response.data.data[0]; // Assuming the first camera for the room
          setStreamUrl(cameraData.stream_url);
          setCameras(response.data.data); // Store all cameras
        } else {
          console.error('No cameras found for this room');
        }
      } catch (error) {
        console.error('Error fetching camera data:', error);
      }
    };

    fetchCameraData();

    // Cleanup the stream connection when leaving the page
    return () => {
      setStreamUrl(null); // This will close the connection by removing the stream URL
    };
  }, [id]); // Depend on `id` to refetch when the room ID changes

  const handleAddCamera = () => {
    if (newCamera.name && newCamera.url) {
      setCameras([...cameras, { ...newCamera, id: Date.now() }]);
      setNewCamera({ name: '', url: '' });
      setShowAddCamera(false);
      simulateUserDetection();
    }
  };

  const handleDeleteCamera = (cameraId) => {
    setCameras(cameras.filter((camera) => camera.id !== cameraId));
  };

  const simulateUserDetection = () => {
    const newUser = {
      id: Date.now(),
      gender: Math.random() > 0.5 ? 'Male' : 'Female',
      age: Math.floor(Math.random() * 60) + 18, // Age between 18 and 78
      clothing: 'Casual', // Example clothing
    };
    setDetectedUsers((prevUsers) => [...prevUsers, newUser]);
    setTimeout(simulateUserDetection, 2000); // Repeat detection every 2 seconds
  };

  if (!room) return <div>Room not found</div>;

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center gap-4 mb-8">
          <Link to="/" className="hover:text-gray-600">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <h1 className="text-2xl font-bold">{room.name}</h1>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Camera Cards */}
          {cameras.map((camera) => (
            <div key={camera.camera_id} className="bg-white rounded-xl shadow-sm p-4">
              <div className="flex justify-between items-start mb-4">
                <h3 className="font-medium">Camera {camera.camera_id}</h3>
                <button
                  onClick={() => handleDeleteCamera(camera.camera_id)}
                  className="text-red-500 hover:text-red-600"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
              <div className="aspect-video bg-gray-100 rounded-lg mb-4 overflow-hidden">
                {/* MJPEG stream using img tag */}
                <img
                  src={camera.stream_url}
                  alt={`Camera ${camera.camera_id}`}
                  className="w-full h-full object-cover"
                />
              </div>
            </div>
          ))}
        </div>

        {/* Detected Users Table */}
        <div className="mt-8">
          <h2 className="text-xl font-bold">Detected Users</h2>
          <table className="min-w-full mt-4 bg-white border border-gray-200">
            <thead>
              <tr>
                <th className="py-2 px-4 border-b">ID</th>
                <th className="py-2 px-4 border-b">Gender</th>
                <th className="py-2 px-4 border-b">Age</th>
                <th className="py-2 px-4 border-b">Clothing</th>
              </tr>
            </thead>
            <tbody>
              {detectedUsers.map((user) => (
                <tr key={user.id}>
                  <td className="py-2 px-4 border-b">{user.id}</td>
                  <td className="py-2 px-4 border-b">{user.gender}</td>
                  <td className="py-2 px-4 border-b">{user.age}</td>
                  <td className="py-2 px-4 border-b">{user.clothing}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default RoomPage;

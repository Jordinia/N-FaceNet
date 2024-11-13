// RoomPage.jsx
import React, { useState } from 'react';
import { ArrowLeft, Plus, Trash2 } from 'lucide-react';
import { Link, useParams } from 'react-router-dom';

const RoomPage = () => {
  // Sample rooms data
  const rooms = [
    { id: 1, name: 'Living Room' },
    { id: 2, name: 'Bedroom' },
    { id: 3, name: 'Kitchen' },
  ];

  const { id } = useParams();
  const room = rooms.find(r => r.id === parseInt(id));
  const [cameras, setCameras] = useState([]);
  const [showAddCamera, setShowAddCamera] = useState(false);
  const [newCamera, setNewCamera] = useState({ name: '', url: '' });
  const [detectedUsers, setDetectedUsers] = useState([]); // Store detected user data

  const handleAddCamera = () => {
    if (newCamera.name && newCamera.url) {
      setCameras([...cameras, { ...newCamera, id: Date.now() }]);
      setNewCamera({ name: '', url: '' });
      setShowAddCamera(false);
      // Simulate user detection for demonstration
      simulateUserDetection();
    }
  };

  const handleDeleteCamera = (cameraId) => {
    setCameras(cameras.filter(camera => camera.id !== cameraId));
  };

  const simulateUserDetection = () => {
    // Simulate detection of users every 2 seconds
    const newUser = {
      id: Date.now(),
      gender: Math.random() > 0.5 ? 'Male' : 'Female',
      age: Math.floor(Math.random() * 60) + 18, // Age between 18 and 78
      clothing: 'Casual', // Example clothing
    };
    setDetectedUsers(prevUsers => [...prevUsers, newUser]);
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
          {cameras.map(camera => (
            <div key={camera.id} className="bg-white rounded-xl shadow-sm p-4">
              <div className="flex justify-between items-start mb-4">
                <h3 className="font-medium">{camera.name}</h3>
                <button 
                  onClick={() => handleDeleteCamera(camera.id)}
                  className="text-red-500 hover:text-red-600"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
              <div className="aspect-video bg-gray-100 rounded-lg mb-4">
                {/* Camera feed would go here */}
                <div className="w-full h-full flex items-center justify-center text-gray-500">
                  <video controls autoPlay src={camera.url} className="w-full h-full" />
                </div>
              </div>
            </div>
          ))}

          {/* Add Camera Button/Form */}
          <div className="bg-gray-100 rounded-xl p-4">
            {showAddCamera ? (
              <div className="space-y-4">
                <h3 className="font-medium">Add New Camera</h3>
                <input
                  type="text"
                  placeholder="Camera Name"
                  className="w-full p-2 rounded border"
                  value={newCamera.name}
                  onChange={e => setNewCamera({ ...newCamera, name: e.target.value })}
                />
                <input
                  type="text"
                  placeholder="Stream URL"
                  className="w-full p-2 rounded border"
                  value={newCamera.url}
                  onChange={e => setNewCamera({ ...newCamera, url: e.target.value })}
                />
                <div className="flex gap-2">
                  <button
                    onClick={handleAddCamera}
                    className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                  >
                    Add Camera
                  </button>
                  <button
                    onClick={() => setShowAddCamera(false)}
                    className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <button
                onClick={() => setShowAddCamera(true)}
                className="w-full h-full flex flex-col items-center justify-center gap-2 text-gray-600 hover:text-gray-800"
              >
                <Plus className="w-8 h-8" />
                <span>Add Camera</span>
              </button>
            )}
          </div>
        </div>

        {/* Detected Users Table */}
        <div className="mt-8 ">
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
              {detectedUsers.map(user => (
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

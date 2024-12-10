import React, { useState, useEffect, useRef } from 'react';
import { ArrowLeft, Plus, Trash2 } from 'lucide-react';
import { Link, useParams } from 'react-router-dom';
import axios from 'axios';
import { Modal, Button, Input } from 'antd';

const RoomPage = () => {
  const [rooms, setRooms] = useState([]); // State untuk menyimpan daftar rooms dari API
  const [streamUrl, setStreamUrl] = useState(null);
  const videoRef = useRef(null);
  const [cameras, setCameras] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [cameraUrl, setCameraUrl] = useState('');
  const { id } = useParams(); // Room ID dari URL params

  // Ambil daftar rooms dari API
  useEffect(() => {
    const fetchRooms = async () => {
      try {
        const response = await axios.get('http://localhost:5000/room');
        if (response.data && response.data.data) {
          setRooms(response.data.data);
        } else {
          console.error('No rooms found');
        }
      } catch (error) {
        console.error('Error fetching rooms:', error);
      }
    };

    fetchRooms();
  }, []);

  // Ambil data kamera untuk ruangan tertentu
  useEffect(() => {
    const fetchCameraData = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/camera/room/${id}`);
        if (response.data && response.data.data.length > 0) {
          setStreamUrl(response.data.data[0].stream_url);
          setCameras(response.data.data);
        } else {
          console.error('No cameras found for this room');
        }
      } catch (error) {
        console.error('Error fetching camera data:', error);
      }
    };

    fetchCameraData();

    return () => {
      setStreamUrl(null);
    };
  }, [id]);

  const openModal = () => {
    setCameraUrl('');
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setCameraUrl('');
  };

  const handleAddCamera = async () => {
    try {
      const response = await axios.post('http://localhost:5000/camera', {
        room_id: id, // Gunakan room ID dari URL params
        camera_url: cameraUrl,
      });

      if (response.status === 200 || response.status === 201) {
        setCameras([...cameras, response.data]); // Asumsikan API mengembalikan kamera yang ditambahkan
        closeModal();
      } else {
        console.error('Failed to add camera');
      }
    } catch (error) {
      console.error('Error adding camera:', error);
    }
  };

  const handleDeleteCamera = (cameraId) => {
    setCameras(cameras.filter((camera) => camera.camera_id !== cameraId));
  };

  const room = rooms.find((r) => r.room_id === parseInt(id)); // Cari room berdasarkan room_id

  if (!room) return <div>Room not found</div>;

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center gap-4 mb-8">
          <Link to="/" className="hover:text-gray-600">
            <ArrowLeft className="w-6 h-6" />
          </Link>
          <h1 className="text-2xl font-bold">{room.room}</h1>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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
                <img
                  src={camera.stream_url}
                  alt={`Camera ${camera.camera_id}`}
                  className="w-full h-full object-cover"
                />
              </div>
            </div>
          ))}

          <div
            className="bg-white rounded-xl shadow-sm p-4 flex items-center justify-center cursor-pointer hover:shadow-md"
            onClick={openModal}
          >
            <Plus className="w-8 h-8 text-gray-500" />
          </div>
        </div>

        <Modal
          title="Add Camera"
          open={isModalOpen}
          onOk={handleAddCamera}
          onCancel={closeModal}
        >
          <div className="flex flex-col gap-4">
            <div>
              <label htmlFor="camera_url">Camera URL</label>
              <Input
                value={cameraUrl}
                onChange={(e) => setCameraUrl(e.target.value)}
                id="camera_url"
                placeholder="Enter Camera URL"
              />
            </div>
          </div>
        </Modal>
      </div>
    </div>
  );
};

export default RoomPage;

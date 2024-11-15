import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import RoomPage from './pages/RoomPage';
import VideoPage from './pages/VideoPage';

function App() {
  const rooms = [/* your rooms data */];
  
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/room/:id" element={<RoomPage rooms={rooms} />} />
        <Route path="/video" element={<VideoPage />} />
      </Routes>
    </Router>
  );
};

export default App;
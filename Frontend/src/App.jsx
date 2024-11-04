import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import RoomPage from './pages/RoomPage';

function App() {
  const rooms = [/* your rooms data */];
  
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/room/:id" element={<RoomPage rooms={rooms} />} />
      </Routes>
    </Router>
  );
};

export default App;
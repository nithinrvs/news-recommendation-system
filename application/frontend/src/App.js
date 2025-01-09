import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Dataset from './components/Dataset';
import Algorithm from './components/Algorithm';
import Signup from './components/Signup';
import Newdashboard from './components/Newdashboard';


function App() {
  return (
    <Router>
      <div>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/dataset" element={< Dataset />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/algorithm" element={< Algorithm />} />
          <Route path="/newdashboard" element={<Newdashboard/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

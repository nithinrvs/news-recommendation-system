import React, { useState, useEffect } from 'react';
import './css/Navbar.css'; // Custom CSS for the navbar
import { Link, useNavigate } from 'react-router-dom';
import NewsLogo from './assests/News.svg';

function Navbar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  // Check the login status when the component mounts and when localStorage changes
  useEffect(() => {
    const checkLoginStatus = () => {
      const loginStatus = localStorage.getItem('isLoggedIn');
      if (loginStatus === 'true') {
        setIsLoggedIn(true);
      } else {
        setIsLoggedIn(false);
      }
    };

    checkLoginStatus();

    // Set up an event listener for changes in localStorage
    window.addEventListener('storage', checkLoginStatus);

    // Cleanup listener when component unmounts
    return () => {
      window.removeEventListener('storage', checkLoginStatus);
    };
  }, []);

  const handleLogout = () => {
    // Remove login state from localStorage and redirect to login page
    localStorage.removeItem('isLoggedIn');
    setIsLoggedIn(false);
    navigate('/');
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <img
          src={NewsLogo}
          alt="Logo"
          className="navbar-logo"
        />
        <span className="navbar-text">NEWS RECOMMENDER SYSTEM</span>
      </div>

      <div className="navbar-center">
        <a href="/" className="navbar-link">Home</a>
        <a href="/dataset" className="navbar-link">Dataset</a>
        <a href="/algorithm" className="navbar-link">Algorithm</a>
      </div>

      <div className="navbar-right">
        {!isLoggedIn ? (
          <Link to="/login" className="login-btn">Login</Link>
        ) : (
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        )}
      </div>
    </nav>
  );
}

export default Navbar;

import React from 'react';
import './css/Navbar.css'; // Custom CSS for the navbar
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <img
          src="https://via.placeholder.com/30" // Replace with actual image URL or logo
          alt="Logo"
          className="navbar-logo"
        />
        <span className="navbar-email">graphic@builder.io</span>
      </div>

      <div className="navbar-center">
        <a href="#features" className="navbar-link">Feature</a>
        <a href="#pricing" className="navbar-link">Pricing</a>
        <a href="#templates" className="navbar-link">Templates</a>
        <a href="#resources" className="navbar-link">Resources</a>
      </div>

      <div className="navbar-right">
        <Link to="/login" className="login-btn">Login</Link> {/* Use Link to navigate to /login */}
      </div>
    </nav>
  );
}

export default Navbar;

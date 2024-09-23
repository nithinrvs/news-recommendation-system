import React, { useState } from 'react';
import './css/Login.css'; 
import { useNavigate } from 'react-router-dom';
import { ReactComponent as MySVG } from './assests/login_image.svg';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://127.0.0.1:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      navigate('/dashboard');  // Navigate to the dashboard on successful login
    } else {
      alert('Invalid login');
    }
  };

  return (
    <div className="login-container">
      <div className="login-left">
        <div className="login-box">
          <h2>Welcome back</h2>
          <p>Please enter your details</p>
          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <label htmlFor="username">Email address</label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="input-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <div className="login-options">
              <div className="remember-me">
                <input type="checkbox" id="remember" />
                <label htmlFor="remember">Remember for 30 days</label>
              </div>
              <a href="#" className="forgot-password">Forgot password?</a>
            </div>
            <button type="submit" className="btn-signin">Log in</button>
          </form>
          <p className="signup-link">
            Don’t have an account? <a href="#">Sign up</a>
          </p>
        </div>
      </div>
      <div className="login-right">
        <div className="login-svg">
          {/* Use the imported SVG as a component */}
          <MySVG width={600} height={600} />
        </div>
      </div>
    </div>
  );
}

export default Login;

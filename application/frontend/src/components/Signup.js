import React, { useState } from 'react';
import './css/Signup.css'; // Create CSS for your signup form or reuse login styles if you want
import { useNavigate } from 'react-router-dom';

function Signup() {
  const [userId, setUserId] = useState('');
  const [categories, setCategories] = useState([]);
  const navigate = useNavigate();

  const availableCategories = [
    'tv', 'sports', 'news', 'video', 'foodanddrink', 'lifestyle',
    'finance', 'autos', 'music', 'health', 'travel', 'entertainment',
    'weather', 'movies', 'kids'
  ];

  const handleCategoryChange = (e) => {
    const value = e.target.value;
    setCategories(prev =>
      prev.includes(value)
        ? prev.filter(category => category !== value)
        : [...prev, value]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://127.0.0.1:8000/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ user_id: userId, favorite_categories: categories }),
    });

    if (response.ok) {
      // Handle successful sign-up
      localStorage.setItem('isSignedUp', 'true');
      navigate('/newdashboard'); // Redirect to dashboard or a relevant page
    } else {
      alert('Sign-up failed');
    }
  };

  return (
    <div className="signup-container">
      <div className="signup-box">
        <h2>Create Your Account</h2>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="userId">Enter User ID</label>
            <input
              type="text"
              id="userId"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
            />
          </div>
          <div className="input-group">
            <label htmlFor="categories">Select Your Favorite Categories</label>
            <div className="categories">
              {availableCategories.map((category) => (
                <div key={category} className="checkbox-group">
                  <input
                    type="checkbox"
                    id={category}
                    value={category}
                    onChange={handleCategoryChange}
                  />
                  <label htmlFor={category}>{category}</label>
                </div>
              ))}
            </div>
          </div>
          <button type="submit" className="btn-signup">Sign up</button>
        </form>
        <p className="login-link">
          Already have an account? <a href="/login">Log in</a>
        </p>
      </div>
    </div>
  );
}

export default Signup;

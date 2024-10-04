import React, { useEffect, useState } from 'react';
import './css/Dashboard.css';

function Dashboard() {
    const [news, setNews] = useState([]);

    useEffect(() => {
        fetch('http://localhost:5000/news') // Adjust the URL if the backend is hosted elsewhere
            .then(response => response.json())
            .then(data => setNews(data))
            .catch(error => console.error('Error fetching news:', error));
    }, []);

    return (
      <div className="dashboard">
          <h1>News Dashboard</h1>
          <div className="news-container">
              {news.map((item) => (
                  <div key={item.news_id} className="news-card">
                      <div className="news-header">
                          <div className="news-category">{item.category}</div>
                          <div className="news-subcategory">{item.subcategory}</div>
                      </div>
                      <div className="news-body">
                          <div className="news-title">{item.title}</div>
                          <a className="news-link" href={item.url} target="_blank" rel="noopener noreferrer">
                              Read More
                          </a>
                      </div>
                  </div>
              ))}
          </div>
      </div>
  );
}

export default Dashboard;

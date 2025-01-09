import React from 'react';
import './css/Home.css';
import NewsPic from './assests/reshot-news-homepage.png';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div>
      <div className="content">
        {/* Left side content */}
        <div className="text-content">
          <h2>Welcome to the News Recommender System</h2>
          <p>A news recommendation system helps users discover relevant articles by analyzing their preferences and reading patterns. It uses machine learning algorithms, such as collaborative filtering or content-based filtering, to predict and suggest articles that align with a user’s interests. These algorithms can learn from a user's behavior, like the types of articles they've read or rated highly, to offer personalized content. By continuously updating its understanding based on user interactions, the system enhances its ability to deliver timely and engaging news.</p>
          {/* Buttons below the content */}
          <div className="buttons-container">
            <Link to="/dataset">
              <button>Dataset</button>
            </Link>
            <Link to="/algorithm">
              <button>Algorithm</button>
            </Link>
          </div>
        </div>

        {/* Right side image */}
        <div className="image-content">
          <img src={NewsPic} alt="News" width={600} height={600} />
        </div>
      </div>
    </div>
  );
}

export default Home;

import React from 'react';
import './Home.css';
import NavBar from './NavBar';
import { Link } from "react-router-dom"; // Import Link from react-router-dom

function Home() {
  return (
    <div className='total'>
      <div className="bg"></div>
      <NavBar />
      <div className='but-cont'>
        <Link to="/yield_estimate" className='butt'>Crop-Yield Estimator</Link>
        <Link to="/disease_detect" className='butt'>Plant Disease Detection</Link>
        <button className='butt' id='ask' onClick={() => window.location.href='http://localhost:8501/'}>
          Ask me anything agriculture
        </button>
      </div>
    </div>
  );
}

export default Home;

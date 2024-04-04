import React from 'react';

import './App.css';
import NavBar from './components/NavBar';
import Detect from './components/pages/Detect';
import Yield from './components/pages/Yield';

function App() {
  return (
    <div className='total'>
      <div className="bg"></div>
      <NavBar />
      <div className='but-cont'>
        <button className='butt' onClick={() => window.location.href='/yield_estimate'} > Crop-Yield Estimator </button>
        <button className='butt' onClick={() => window.location.href='/disease_detect'} > Plant Disease Detection </button>
        <button className='butt' id='ask' onClick={() => window.location.href='http://localhost:8501/'}> ask me anything agriculture </button>
      </div>
    </div>
  );
}

export default App;

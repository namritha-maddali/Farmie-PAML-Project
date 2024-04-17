import React, { useState } from 'react';
import './Yield.css'; 

function Yield() {

  const [state, setState] = useState('');
  const [district, setDistrict] = useState('');
  const [crop, setCrop] = useState('');
  const [season, setSeason] = useState('');
  const [area, setArea] = useState('');
  const [unit, setUnit] = useState('hectares');
  const [yieldEstimate, setYieldEstimate] = useState(null);
  const [productionEstimate, setProductionEstimate] = useState(null);

  const handleInputChange = (event) => {
    const { name, value } = event.target;
  
    switch (name) {
      case 'state':
        setState(value);
        break;
      case 'district':
        setDistrict(value);
        break;
      case 'crop':
        setCrop(value);
        break;
      case 'season':
        setSeason(value);
        break;
      case 'area':
        setArea(value);
        break;
      case 'unit':
        setUnit(value);
        break;
      default:
        break;
    }
  };


  const handleSubmit = async (event) => {
  
    event.preventDefault();
    console.log('Form submitted!');
  
    let adjustedArea = parseFloat(area);
    if (unit === 'acres') {
      adjustedArea *= 0.4;
    }
    const response = await fetch('/api/yieldEstimation', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ state, district, crop, season, area: adjustedArea }),
    });
    const data = await response.json();
  
    setYieldEstimate(data.yield);
    setProductionEstimate(data.production);
  };

  return (
    <div className="yield">
      <h2>Crop Yield Estimation</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Enter your state:</label>
          <input
            type="text"
            name="state"
            value={state}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label>Enter your district:</label>
          <input
            type="text"
            name="district"
            value={district}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label>Enter the name of the crop:</label>
          <input
            type="text"
            name="crop"
            value={crop}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label>Which season are you growing the crop in?</label>
          <select name="season" value={season} onChange={handleInputChange}>
            <option value="">Select Season</option>
            <option value="0">Kharif</option>
            <option value="1">Rabi</option>
            <option value="2">Zaid</option>
            <option value="3">Whole Year</option>
          </select>
        </div>
        <div>
          <label>What is the area of the land where you're growing this crop:</label>
          <input
            type="text"
            name="area"
            value={area}
            onChange={handleInputChange}
          />
          <select name="unit" value={unit} onChange={handleInputChange}>
            <option value="hectares">Hectares</option>
            <option value="acres">Acres</option>
          </select>
        </div>
        <button type="submit">Estimate Yield</button>
      </form>

      {yieldEstimate !== null && productionEstimate !== null && (
        <div>
          <h3>Estimates</h3>
          <p>Yield Estimate: {yieldEstimate} tonnes per hectare</p>
          <p>Production Estimate: {productionEstimate} tonnes</p>
        </div>
      )}
    </div>
  );
}

export default Yield;

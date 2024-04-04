import './NavBar.css';
import profile from '../profile.png';

function NavBar() {
  return (
    <div className="nav">
      <div className='links'>
        <button className='link' onClick={() => window.location.href='/'} > Home </button>
        <button className='link' onClick={() => window.location.href='/about'} > About </button>
        <button className='link' onClick={() => window.location.href='/yield_estimate'} > Crop-Yield Estimator </button>
        <button className='link' onClick={() => window.location.href='/disease_detect'} > Plant Disease Detection </button>
        <img src={profile} height='45' width='45' className='prof' onClick={() => window.location.href='/login'}/>
      </div>
    </div>
  );
}

export default NavBar;
import React from "react";
import { BrowserRouter as Router, Route, Routes} from "react-router-dom";

import Home from "./components/Home";
import NavBar from "./components/NavBar";

import Detect from "./components/pages/Detect";
import Yield from './components/pages/Yield';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path="/yield_estimate" element={<Yield/>} />
        <Route path='/disease_detect' element={<Detect />} />
      </Routes>
    </Router>
  );
}

export default App;

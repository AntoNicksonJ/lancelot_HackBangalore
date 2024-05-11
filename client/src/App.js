import React from 'react';
import './App.css';
import NavigationBar from './components/Nav/NavigationBar';
import Welcome from './components/Welcome/Welcome';
import Scheam from './components/sceambot/sccheam';
import AboutSection from './components/About/AboutSection';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';















function App() {


  return (
    <div className='App'>
  <Router>
  <Routes>
  <Route path="/" element={
  <React.Fragment>
    <NavigationBar/>
    <Welcome/>
    <AboutSection/>
  </React.Fragment>

} />


<Route path="/home" element={
  <React.Fragment>
    <NavigationBar/>
    <Scheam/>
  </React.Fragment>

} />

  </Routes>
  </Router>
    </div>
  );
} 
export default App;
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

<Route path="/detail2" element={
  <React.Fragment>
    <NavigationBar/>
    <Nav/>
    <User/>
    </React.Fragment>
} />

<Route path="/detail3" element={
  <React.Fragment>
    <NavigationBar/>
    <Nav/>
    <Address/>
    </React.Fragment>
} />

<Route path="/detail4" element={
  <React.Fragment>
    <NavigationBar/>
    <Nav/>
    <Income/>
    </React.Fragment>
} />

<Route path="/detail5" element={
  <React.Fragment>
    <NavigationBar/>
    <Nav/>
    <Pdf/>
    </React.Fragment>

} />

  </Routes>
  </Router>
    </div>
  );
} 
export default App;


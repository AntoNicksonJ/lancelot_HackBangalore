import React from 'react';
import './Bar.css'
import { Link } from 'react-router-dom';
class NavBar extends React.Component {
  render() {
    return (
      <div className='bo2'>
        <nav className='naan'>
        <ul>
          <li><a href="#"><Link to="/detail">Identity</Link></a></li>
          <li><a href="#"><Link to="/detail2">User ID</Link></a></li>
          <li><a href="#"><Link to="/detail3">Address</Link></a></li>
          <li><a href="#"><Link to="/detail4">Income</Link></a></li>
          <li><a href="#"><Link to="/detail5">Proposal</Link></a></li>
        </ul>
      </nav>
      </div>
    );
  }
}

export default NavBar;
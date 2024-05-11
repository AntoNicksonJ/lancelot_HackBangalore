import React, { useState } from 'react';
import axios from 'axios';
// import './Identity.css';
import { Link } from 'react-router-dom';

function App() {
  
  return (
    <div className='bo3'>
      <form className='nsd'>
        <h2>Proof of Address</h2>
        <h6>Rental Address</h6>
        <input type="text" name="input1" />
        <h6>Lease address</h6>
        <input type="text" name="input2"  />
        {/* <h6> ID</h6>
        <input type="text" name="input3" value={inputs.input3} onChange={handleChange} /> */}
        {/* <input type="file" onChange={handleFileChange} /> */}
        <button type="submit">Submit</button>
        <button type="submit" className="next"><Link to="/detail4"><a>Next</a></Link></button>
      </form>
    </div>
  );
}

export default App;
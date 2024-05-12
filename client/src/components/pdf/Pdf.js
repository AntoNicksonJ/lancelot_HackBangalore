import React, { useState } from 'react';
import axios from 'axios';
import './Pdf.css';


function App() {
  const [inputText1, setInputText1] = useState('');
  const [inputText2, setInputText2] = useState('');
  const [displayText1, setDisplayText1] = useState('');
  const [displayText2, setDisplayText2] = useState('');

  const handleChange1 = (event) => {
    setInputText1(event.target.value);
  };

  const handleChange2 = (event) => {
    setInputText2(event.target.value);
  };

  const handleSubmit1 = () => {
    axios.post('/api/submit1', { text: inputText1 })
      .then(response => {
        setDisplayText1(response.data.text);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  const handleSubmit2 = () => {
    axios.post('/api/submit2', { text: inputText2 })
      .then(response => {
        setDisplayText2(response.data.text);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  const handleDisplay1 = () => {
    axios.get('/api/display1')
      .then(response => {
        setDisplayText1(response.data.text);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  const handleDisplay2 = () => {
    axios.get('/api/display2')
      .then(response => {
        setDisplayText2(response.data.text);
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  const sendEmail = () => {
    axios.post('/send-email')
        .then(response => {
            console.log(response.data);
            alert('Email sent successfully');
        })
        .catch(error => {
            console.error('Successfully sending email:', error);
            alert('Email sent successfully');
        });
}


  return (
    <div className='niks'>
    <div class="bo33">
    <div className='bbbbb'>
    
        <textarea placeholder=' Enter Ur business proposal 
        Executive Summary       Organization and Management
        Service or Product      Marketing and Sales
        Financing Analysis      Funding Request
        Company Description     Market Plan and Analysis
        Appendix
        ' className=".bosss2" type="text" value={inputText1} onChange={handleChange1} />
        <button onClick={handleSubmit1}>Submit</button>
        {/* <button onClick={handleDisplay1}>Display 1</button> */}
        <div className='Bosss3'>
          <h3>Fill these missing datas in the following column </h3>
          <p >{displayText1}</p></div>
      
        <textarea placeholder='Missed Data Column' className=".bosss2" type="text" value={inputText2} onChange={handleChange2} />
        <button onClick={handleSubmit2}>Submit</button>
        {/* <button onClick={handleDisplay2}>Display 2</button> */}
        
        <div className='Bosss3'>
        <h3>The Inference of the proposal</h3>
          <p >{displayText2}</p></div>
        <button onClick={sendEmail}>Send Email</button>
    
    </div>
    </div>
    </div>
   
  );
}

export default App;
import React, { useState } from 'react';
import axios from 'axios';
import './sccheam.css'

function App() {
  const [inputText, setInputText] = useState('');
  const [textInfo, setTextInfo] = useState({});
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('/sort_words', { text: inputText });
      setTextInfo(response.data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div class="bo">
      <div class="b"  >
      <h1>Help you find the best SME Scheam</h1>
      <form onSubmit={handleSubmit}>
        <p>Enter loan for :</p>
        <label>
        <textarea className='search' placeholder='Enter the detail about your loan' value={inputText} onChange={(e) => setInputText(e.target.value)} style={{ resize: 'none' }} />
        </label>
        <button type="submit">Get Answer</button>
      </form>

      {loading && <p>Loading...</p>}

      {textInfo.original_text && (
        <div className='use'>
          <p className="Hed">Query</p>
          <p>{textInfo.original_text}</p>
        </div>
      )}
      {textInfo.sorted_text && (
        <div className='output'>
          <p className="Hed Hed2">This information help you to find out the best scheam for your SME</p>
          <p>{textInfo.sorted_text}</p>
        </div>
      )}
      </div>
    </div>
  );
}

export default App;
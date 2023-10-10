import React, { useState } from 'react';
import Dropdown from './components/Dropdown/Dropdown';
import axios from 'axios';
import './App.css';

function App() {
  const [message, setMessage] = useState("");
  const [data, setData] = useState(null);  

  const options = [
    { label: "TRITANIUM", value: "TRITANIUM" },
    { label: "PYERITE", value: "PYERITE" },
    // ... add more options as needed
  ];

  const handleDropdownChange = async (selectedValue) => {
    try {
      const response = await axios.get(`http://127.19.0.2:5000/get_item/${selectedValue}`);
      setData(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div className="App">
      <h1>My React App</h1>
      <Dropdown options={options} onChange={handleDropdownChange} />
      {data && (
        <div>
          <h2>Item Data:</h2>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
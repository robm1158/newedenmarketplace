import React, { useState } from 'react';
import Dropdown from './components/Dropdown/Dropdown';
import DataTable from './components/DataTable/DataTable';
import axios from 'axios';
import './App.css';

// Import the enum
import { ItemEnum } from './constants/ItemEnum';

function App() {
  const [data, setData] = useState(null);  

  // Convert the Enum to dropdown options format using the keys
  const options = Object.keys(ItemEnum).map(key => ({
    label: key,
    value: key,
  }));

  const handleDropdownChange = async (selectedValue) => {
    console.log("Selected value:", selectedValue);
    try {
      const response = await axios.get(`http://127.0.0.1:5000/get_item/${selectedValue}`);
      setData(response.data);
      console.log("Fetched data:", response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div className="App">
      <h1>My React App</h1>
      <Dropdown options={options} onChange={handleDropdownChange} />
      {data && data.length > 0 && <DataTable data={data} />}
      <a href="/dashboard/" target="_blank">Go to Dashboard</a>
    </div>
  );
}

export default App;

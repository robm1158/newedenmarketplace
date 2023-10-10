import React, { useState } from 'react';
import Dropdown from './components/Dropdown/Dropdown';
import DataTable from './components/DataTable/DataTable';
// import DashIframe from './components/DashIframe/DashIframe';
import Graph from './components/Graph/Graph';
import { ItemEnum } from './constants/ItemEnum';
import PagedTable from './components/PagedTable/PagedTable';
import axios from 'axios';
import './App.css';


function App() {
  const [tableData, setTableData] = useState(null);
  const [graphData, setGraphData] = useState(null);

  // Convert the Enum to dropdown options format using the keys
  const options = Object.keys(ItemEnum).map(key => ({
    label: key,
    value: key,
  }));

  // These are moved outside of the handleDropdownChange function
  const buyOrders = tableData ? tableData.filter(order => order.is_buy_order === true) : [];
  const nonBuyOrders = tableData ? tableData.filter(order => order.is_buy_order === false) : [];
  console.log("buy orders*:", buyOrders);
  console.log("non buy orders*:", nonBuyOrders);

  const handleDropdownChange = async (selectedValue) => {
    console.log("Selected value*:", selectedValue);
    console.log("Graph data*:", graphData);

    try {
      // Endpoint for fetching table data
      const tableResponse = await axios.get(`http://127.0.0.1:5000/get_item/${selectedValue}`);
      setTableData(tableResponse.data);
      console.log("Table data:", tableData);

      // Endpoint for fetching graph data - using POST as expected by Flask
      const graphResponse = await axios.post(`http://127.0.0.1:5000/get_graph_data`, { selectedValue: selectedValue });
      setGraphData(graphResponse.data);
      console.log("Graph data:", graphData);

    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div className="App">
        <h1>My React App</h1>
        <Dropdown options={options} onChange={handleDropdownChange} />
        <div style={{ display: "flex", justifyContent: 'center'}}>
          {graphData && <Graph data={graphData} />}
        </div>
        
        <div style={{ display: 'flex', justifyContent: 'space-evenly' }}>
          
            <div>
                <h2>Buy Orders</h2>
                <PagedTable data={buyOrders} headers={['issued', 'station_id', 'price']} />
            </div>
            <div>
                <h2>Sell Orders</h2>
                <PagedTable data={nonBuyOrders} headers={['issued', 'station_id', 'price']} />
            </div>
        </div>

        
    </div>
);

}

export default App;

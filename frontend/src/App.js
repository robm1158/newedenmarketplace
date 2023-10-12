import React, { useState } from 'react';
// import Dropdown from './components/Dropdown/Dropdown';
// import { Routes, Route } from 'react-router-dom';
import Graph from './components/Graph/Graph';
import { ItemEnum } from './constants/ItemEnum';
import PagedTable from './components/PagedTable/PagedTable';
import { ColorModeContext, useMode } from './theme';
import { CssBaseline, ThemeProvider } from '@mui/material';
import Topbar from './scenes/global/Topbar';
import CustomSidebar from "./scenes/global/Sidebar";
// import { Dashboard } from "./scenes/dashboard";
import axios from 'axios';
import './App.css';

function App() {
  const [tableData, setTableData] = useState(null);
  const [graphData, setGraphData] = useState(null);
  const [theme, colorMode] = useMode();

  const options = Object.keys(ItemEnum).map(key => ({
    label: key,
    value: key,
  }));

  const buyOrders = tableData ? tableData.filter(order => order.is_buy_order === true) : [];
  const nonBuyOrders = tableData ? tableData.filter(order => order.is_buy_order === false) : [];
    
  const handleSidebarClick = async (selectedValue) => {
    // You might use the type_id here to fetch relevant data
    try {
        const tableResponse = await axios.get(`http://127.0.0.1:5000/get_item/${selectedValue}`);
        setTableData(tableResponse.data);

        const graphResponse = await axios.post(`http://127.0.0.1:5000/get_graph_data`, { selectedValue: selectedValue });
        setGraphData(graphResponse.data);
      
    } catch (error) {
        console.error("Error fetching data:", error);
    }
};


  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="App">
          <Topbar />
          <div className="mainWrapper">
            <div className="sidebar">
            <CustomSidebar handleSidebarClick={handleSidebarClick} setTableData={setTableData} setGraphData={setGraphData} />

            </div>
            <main className='content'>
              <h1>My React App </h1>
              <div style={{ display: "flex", justifyContent: 'center' }}>
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
            </main>
          </div>
        </div>
      </ThemeProvider>
    </ColorModeContext.Provider>
);
}

export default App;

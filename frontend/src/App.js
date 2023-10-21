import React, { useState } from 'react';
import Graph from './components/Graph/Graph';
import { ItemEnum } from './constants/ItemEnum';
import PagedTable from './components/PagedTable/PagedTable';
import { ColorModeContext, useMode } from './theme';
import { CssBaseline, ThemeProvider } from '@mui/material';
import Topbar from './scenes/global/Topbar';
import CustomSidebar from "./scenes/global/Sidebar";
import axios from 'axios';
import './App.css';

function App() {
  const [tableData, setTableData] = useState(null);
  const [graphData, setGraphData] = useState(null);
  const [theme, colorMode] = useMode();
  const [selectedItemName, setSelectedItemName] = useState(null);

  const options = Object.keys(ItemEnum).map(key => ({
    label: key,
    value: key,
  }));

  const REVERSED_ITEM_ENUM = Object.keys(ItemEnum).reduce((obj, key) => {
    obj[ItemEnum[key]] = key;
    return obj;
}, {});

  const buyOrders = tableData ? tableData.filter(order => order.is_buy_order === true) : [];
  const nonBuyOrders = tableData ? tableData.filter(order => order.is_buy_order === false) : [];
    
  const handleSidebarClick = async (selectedValue) => {
    const name = REVERSED_ITEM_ENUM[selectedValue];
    setSelectedItemName(name);
    // You might use the type_id here to fetch relevant data
    try {
        const tableResponse = await axios.get(`http://127.0.0.1:5000/get_item/${name}`);
        setTableData(tableResponse.data);

        const graphResponse = await axios.post(`http://127.0.0.1:5000/get_graph_data`, { selectedValue: name });
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
              <div style={{ display: "flex"}}>
                {graphData && <Graph data={graphData} itemName={selectedItemName}/>}
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

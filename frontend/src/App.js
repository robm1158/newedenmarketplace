import React, { useState } from 'react';
import Graph from './components/Graph/Graph';
import { ItemEnum } from './constants/ItemEnum';
import PagedTable from './components/PagedTable/PagedTable';
import { LocationEnum } from '/root/code/eve-aws/frontend/src/constants/locationEnum';
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

  function transformDataWithLocation(data) {
    return data.map(row => {
      // Replace the location_id with the corresponding string from LocationEnum
      // If the ID doesn't exist in the enum, it will leave the id as is.
      const locationName = LocationEnum[row.location_id] || row.location_id;
      return {
        ...row,
        location_id: locationName,
      };
    });
  }


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
              {/* <h1>My React App </h1> */}
              <div style={{ display: "flex"}}>
                {graphData && <Graph data={graphData} itemName={selectedItemName}/>}
              </div>
              
              <div class="flex-container" style={{ display: 'flex', justifyContent: 'left' }}>
                  <div>
                      <h2>Sell Orders</h2>
                      <PagedTable  data={transformDataWithLocation(nonBuyOrders)} headers={[
                        { displayName: 'Date', dataKey: 'issued' },
                        { displayName: 'Order ID', dataKey: 'order_id' },
                        { displayName: 'Location', dataKey: 'location_id' },
                        { displayName: 'Price', dataKey: 'price' },
                        { displayName: 'Volume', dataKey: 'volume_remain'}
                      ]} />
                  </div>
              </div>  
              <div class="flex-container" style={{ display: 'flex', justifyContent: 'left' }}>
                  <div>
                      <h2>Buy Orders</h2>
                      <PagedTable data={transformDataWithLocation(buyOrders)} headers={[
                              { displayName: 'Date', dataKey: 'issued' },
                              { displayName: 'Order ID', dataKey: 'order_id' },
                              { displayName: 'Location', dataKey: 'location_id' },
                              { displayName: 'Price', dataKey: 'price' },
                              { displayName: 'Volume', dataKey: 'volume_remain'}
                            ]} />
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

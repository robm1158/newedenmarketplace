import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
// import Graph from './components/Graph/Graph';
// import BubbleGraph from './components/BubbleGraph/BubbleGraph';
import { ItemEnum } from './constants/ItemEnum';
// import PagedTable from './components/PagedTable/PagedTable';
import Home from './components/Home/Home';
import { LocationEnum } from './constants/locationEnum';
import { ColorModeContext, useMode } from './theme';
import { CssBaseline, ThemeProvider } from '@mui/material';
import Topbar from './scenes/global/Topbar';
import CustomSidebar from "./scenes/global/Sidebar";
import Dashboard from "./components/Dashboard/Dashboard";
import axios from 'axios';
import './App.css';

function App() {
  const [tableData, setTableData] = useState(null);
  const [graphData, setGraphData] = useState(null);
  const [bubbleGraphData, setBubbleGraphData] = useState(null);
  const [theme, colorMode] = useMode();
  const [selectedItemName, setSelectedItemName] = useState(null);

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
  // const options = Object.keys(ItemEnum).map(key => ({
  //   label: key,
  //   value: key,
  // }));

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
    
  const handleSidebarClick = async (selectedValue, itemType) => {
    console.log("Selected Value:", selectedValue, "Item Type:", itemType);

    const name = REVERSED_ITEM_ENUM[selectedValue];
    console.log("Selected Name:", name);
    setSelectedItemName(name);
    if (!name) {
      console.error(`No name found for selectedValue: ${selectedValue}`);
      return;
  }
    // You might use the type_id here to fetch relevant data
    try {
        const tableResponse = await axios.get(`${BACKEND_URL}/get_item/${name}`);
        setTableData(tableResponse.data);

        const graphResponse = await axios.post(`${BACKEND_URL}/get_graph_data`, { selectedValue: name });
        setGraphData(graphResponse.data);

        // Adding itemType to the request payload for bubble graph data
        const bubbleGraphResponse = await axios.post(`${BACKEND_URL}/get_bubble_data`, { 
            selectedValue: selectedValue,
            itemType: itemType // include the itemType in the request
        });
        setBubbleGraphData(bubbleGraphResponse.data);
    } catch (error) {
        console.error("Error fetching data:", error);
    }
};

return (
  <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
          <CssBaseline />
          <Router>
              <div className="App">
                  <Topbar />
                  <div className="mainWrapper">
                      <div className="sidebar">
                          <CustomSidebar handleSidebarClick={handleSidebarClick} setTableData={setTableData} setGraphData={setGraphData} />
                      </div>
                      <main className='content'>
                          <Routes>
                              <Route path="/" element={<Home />} exact />
                              <Route path="/dashboard" element={
                                  <Dashboard 
                                      graphData={graphData}
                                      selectedItemName={selectedItemName}
                                      nonBuyOrders={nonBuyOrders}
                                      bubbleGraphData={bubbleGraphData}
                                      buyOrders={buyOrders}
                                      transformDataWithLocation={transformDataWithLocation}
                                  />
                              } />
                              {/* ... Other routes ... */}
                          </Routes>
                      </main>
                  </div>
              </div>
          </Router>
      </ThemeProvider>
  </ColorModeContext.Provider>
);
}

export default App;
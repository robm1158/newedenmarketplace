import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import { ItemEnum } from './constants/ItemEnum';
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

  const REVERSED_ITEM_ENUM = Object.keys(ItemEnum).reduce((obj, key) => {
    obj[ItemEnum[key]] = key;
    return obj;
  }, {});

  function transformDataWithLocation(data) {
    return data.map(row => {
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
    // ... existing logic ...
  };

  function MainContent() {
    const location = useLocation();

    return (
      <div className="App">
        <Topbar />
        <div className="mainWrapper">
          <div className="sidebar">
            {location.pathname !== "/" && (
              <CustomSidebar handleSidebarClick={handleSidebarClick} setTableData={setTableData} setGraphData={setGraphData} />
            )}
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
    );
  }

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <MainContent />
        </Router>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export default App;

import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import Home from './components/Home/Home';
import { ItemEnum } from './constants/ItemEnum';
import { LocationEnum } from './constants/locationEnum';
import { ColorModeContext, useMode } from './theme';
import { CssBaseline, ThemeProvider } from '@mui/material';
import Topbar from './scenes/global/Topbar';
import CustomSidebar from "./scenes/global/Sidebar";
import Dashboard from "./components/Dashboard/Dashboard";
import axios from 'axios';
import './App.css';

function MainContent() {
    const [tableData, setTableData] = useState(null);
    const [graphData, setGraphData] = useState(null);
    const [bubbleGraphData, setBubbleGraphData] = useState(null);
    const [selectedItemName, setSelectedItemName] = useState(null);
    const location = useLocation();
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
        const name = REVERSED_ITEM_ENUM[selectedValue];
        setSelectedItemName(name);
        if (!name) {
            console.error(`No name found for selectedValue: ${selectedValue}`);
            return;
        }
        try {
            if (itemType === "type" ){
                const tableResponse = await axios.get(`${BACKEND_URL}/get_item/${name}/${itemType}`);
                setTableData(tableResponse.data);
                const graphResponse = await axios.post(`${BACKEND_URL}/get_graph_data`, { selectedValue: name });
                setGraphData(graphResponse.data);
                const bubbleGraphResponse = await axios.post(`${BACKEND_URL}/get_bubble_data`, { 
                    selectedValue: selectedValue,
                    itemType: itemType
                });
                setBubbleGraphData(bubbleGraphResponse.data);
            }
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    return (
        <div className="App">
            <Topbar />
            <div className="mainWrapper">
                {
                    location.pathname !== "/" && (
                        <div className="sidebar">
                            <CustomSidebar handleSidebarClick={handleSidebarClick} setTableData={setTableData} setGraphData={setGraphData} />
                        </div>
                    )
                }
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

function App() {
    const [theme, colorMode] = useMode();

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

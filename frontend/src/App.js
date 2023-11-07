import React, { useState} from 'react';
import { BrowserRouter as Router, Route, Routes,useLocation } from 'react-router-dom';
import Home from './components/Home/Home';
import Aboutme from './components/Aboutme/Aboutme';
import AuthCallbackPage from './components/AuthCallbackPage/AuthCallbackPage';
import UserProfile from './components/UserProfile/UserProfile';
import AuthProvider  from './components/AuthProvider/AuthProvider';
import { PrivateRoute } from './components/PrivateRoute/PrivateRoute';
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
        
        if (itemType === "type") {
            const name = REVERSED_ITEM_ENUM[selectedValue];
            setSelectedItemName(name);
            if (!name) {
                console.error(`No name found for selectedValue: ${selectedValue}`);
                return;
            }        
            try {
                const tableResponse = await axios.get(`${BACKEND_URL}/get_item/${name}/${itemType}`);
                setTableData(tableResponse.data);
    
                const graphResponse = await axios.post(`${BACKEND_URL}/get_graph_data`, { 
                    selectedValue: name,
                    itemType: itemType
                });
                setGraphData(graphResponse.data);
    
                const bubbleGraphResponse = await axios.post(`${BACKEND_URL}/get_bubble_data`, { 
                    selectedValue: selectedValue,
                    itemType: itemType
                });
                setBubbleGraphData(bubbleGraphResponse.data);
    
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        } else {
            // Handle the situation when itemType is not 'type', if necessary
            console.log(`The itemType is not 'type', it is '${itemType}'. No data will be fetched.`);
        }
    };

    return (
        <div className="App">
            <Topbar />
            <div className="mainWrapper">
                {
                    location.pathname !== "/" && location.pathname !== "/aboutme" && location.pathname !== "/userprofile" && (
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
                        <Route path="/aboutme" element={<Aboutme />} exact />
                        <Route path="/callback" element={<AuthCallbackPage />} />
                        <Route
    path="/userprofile"
    element={
      <PrivateRoute>
        <UserProfile />
      </PrivateRoute>
    }
  />
                    </Routes>
                </main>
            </div>
        </div>
    );
}

function App() {
    const [theme, colorMode] = useMode();

    return (
        <AuthProvider>
            <ColorModeContext.Provider value={colorMode}>
                <ThemeProvider theme={theme}>
                    <CssBaseline />
                    <Router>
                        <MainContent />
                    </Router>
                </ThemeProvider>
            </ColorModeContext.Provider>
        </AuthProvider>
    );
}

export default App;

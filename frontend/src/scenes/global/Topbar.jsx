import { Box, Typography, IconButton } from '@mui/material';
import SsidChartOutlinedIcon from '@mui/icons-material/SsidChartOutlined';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { useNavigate } from 'react-router-dom';
import homeIcon from '../../assets/images/Transparent_White.png';
import loginIcon from '../../assets/images/eve-sso-login-black-large.png';
import React, { useState } from 'react';

const Topbar = ({ ...props }) => {
    const navigate = useNavigate();
    const [anchorEl, setAnchorEl] = useState(null);

    const handleOpenMenu = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleCloseMenu = () => {
        setAnchorEl(null);
    };

    const handleLogin = () => {
        const clientId = process.env.REACT_APP_EVE_CLIENT_ID;
        const callbackUrl = encodeURIComponent(process.env.REACT_APP_CALLBACK_URL);
        const SCOPES = encodeURIComponent('publicData esi-wallet.read_character_wallet.v1 esi-markets.read_character_orders.v1');
        const STATE = 'uniquestate9876';
        const loginUrl = `https://login.eveonline.com/v2/oauth/authorize/?response_type=code&redirect_uri=${callbackUrl}&client_id=${clientId}&scope=${SCOPES}&state=${STATE}`;

        window.location.href = loginUrl; // Redirects the user to the EVE SSO login page
      };

    return (
        <Box display="flex" justifyContent="space-between" p={2} alignItems="center"> 
            {/* Home and Search Bar */}
            <Box display="flex" alignItems="center" flexShrink={0}> 
                <IconButton onClick={() => navigate("/")}>
                    <img src={homeIcon} alt="Home" style={{ width: '196px', height: '42px' }} /> {/* PNG image as home button */}
                </IconButton>
            </Box>
            
            {/* Center Box: Use flexGrow to allow this Box to take available space */}
            <Box display="flex" justifyContent="center" flexGrow={1}>
                <IconButton onClick={() => navigate("/dashboard")}>
                    <SsidChartOutlinedIcon />
                    <Typography variant="body1" style={{ marginLeft: '8px' }}>Analytics</Typography>
                </IconButton>
                <IconButton onClick={handleOpenMenu}>
                    <Typography variant="body1">Tools</Typography>
                </IconButton>
                <Menu
                    anchorEl={anchorEl}
                    open={Boolean(anchorEl)}
                    onClose={handleCloseMenu}
                >
                    <MenuItem onClick={handleCloseMenu}>Appraisal</MenuItem>
                    <MenuItem onClick={handleCloseMenu}>Option 2</MenuItem>
                    <MenuItem onClick={handleCloseMenu}>Option 3</MenuItem>
                    {/* Add more MenuItem components for more options */}
                </Menu>
                <IconButton onClick={() => navigate("/aboutme")}>
                    <Typography variant="body1">About Me</Typography>
                </IconButton>
                <IconButton onClick={() => navigate("/userprofile")}>
                    <Typography variant="body1">My Profile</Typography>
                </IconButton>
            </Box>
    
            <Box flexShrink={0}>
                <IconButton onClick={handleLogin}>
                    <img src={loginIcon} alt="Login" style={{ width: '196px', height: '38px' }} />
                </IconButton>
            </Box>
        </Box>
    )
}

export default Topbar;

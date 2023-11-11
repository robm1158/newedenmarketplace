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
    const [contactAnchorEl, setContactAnchorEl] = useState(null);

    const handleOpenMenu = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleCloseMenu = () => {
        setAnchorEl(null);
    };

    const handleOpenContactMenu = (event) => {
        setContactAnchorEl(event.currentTarget);
    };

    const handleCloseContactMenu = () => {
        setContactAnchorEl(null);
    };

    const handleLogin = () => {
        // ... Your existing login handler code ...
    };

    return (
        <Box display="flex" justifyContent="space-between" p={2} alignItems="center"> 
            {/* Home and Search Bar */}
            <Box display="flex" alignItems="center" flexShrink={0}> 
                <IconButton onClick={() => navigate("/")}>
                    <img src={homeIcon} alt="Home" style={{ width: '196px', height: '42px' }} />
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
                </Menu>
                <IconButton onClick={() => navigate("/userprofile")}>
                    <Typography variant="body1">My Profile</Typography>
                </IconButton>
                <IconButton onClick={handleOpenContactMenu}>
                    <Typography variant="body1">Contact Us</Typography>
                </IconButton>
                <Menu
                    anchorEl={contactAnchorEl}
                    open={Boolean(contactAnchorEl)}
                    onClose={handleCloseContactMenu}
                >
                    <MenuItem onClick={() => {handleCloseContactMenu(); navigate("/howto");}}>How To</MenuItem>
                    <MenuItem onClick={() => {handleCloseContactMenu(); navigate("/aboutme");}}>About Me</MenuItem>
                    <MenuItem onClick={handleCloseContactMenu}>FAQ</MenuItem>
                </Menu>
                
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

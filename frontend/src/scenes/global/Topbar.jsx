import { Box, Typography, IconButton } from '@mui/material';
import NotificationsOutlinedIcon from '@mui/icons-material/NotificationsOutlined';
import SearchOutlinedIcon from '@mui/icons-material/SearchOutlined';
import SpaceDashboardOutlinedIcon from '@mui/icons-material/SpaceDashboardOutlined';
import SsidChartOutlinedIcon from '@mui/icons-material/SsidChartOutlined';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { useNavigate } from 'react-router-dom';
import homeIcon from '../../assets/images/Statik_Logo_grey.png';
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

    return (
        <Box display="flex" justifyContent="space-between" p={1} alignItems="center"> 
            {/* Home and Search Bar */}
            <Box display="flex" alignItems="center" flexShrink={0}> 
                <IconButton onClick={() => navigate("/")}>
                    <img src={homeIcon} alt="Home" style={{ width: '32px', height: '32px' }} /> {/* PNG image as home button */}
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
                <IconButton>
                    <Typography variant="body1">About Me</Typography>
                </IconButton>
            </Box>
    
            <Box flexShrink={0}>
                <IconButton>
                    <Typography variant="body1" style={{ marginLeft: '8px' }}>Login Place Holder</Typography>
                </IconButton>
            </Box>
        </Box>
    )
}

export default Topbar;

import { Box, IconButton, useTheme } from '@mui/material';
import { useContext } from 'react';
import { ColorModeContext, tokens } from '../../theme';
import InputBase from '@mui/material/InputBase';
import LightModeOutlinedIcon from '@mui/icons-material/LightModeOutlined';
import DarkModeOutlinedIcon from '@mui/icons-material/DarkModeOutlined';
import NotificationsOutlinedIcon from '@mui/icons-material/NotificationsOutlined';
import SearchOutlinedIcon from '@mui/icons-material/SearchOutlined';
import SpaceDashboardOutlinedIcon from '@mui/icons-material/SpaceDashboardOutlined';
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined'; // <-- Import the new icon
import { useNavigate } from 'react-router-dom';
import homeIcon  from '../../assets/images/Statik_Logo_grey.png';


const Topbar = ({ ...props }) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const colorMode = useContext(ColorModeContext);
    const navigate = useNavigate();

    return (
        <Box display="flex" justifyContent="space-between" p={2}> 
            {/* Home and Search Bar */}
            <Box display="flex" alignItems="center"> 
                <IconButton onClick={() => navigate("/")}>
                    <img src={homeIcon} alt="Home" style={{ width: '24px', height: '24px' }} /> {/* PNG image as home button */}
                </IconButton>
                <Box display="flex" backgroundColor={colors.primary[300]} borderRadius="3" ml={1}>
                    <InputBase sx={{ml: 2, flex: 1}} placeholder="Search..." />
                    <IconButton type="button" sx={{p: 1}}>
                        <SearchOutlinedIcon />
                    </IconButton>
                </Box>
            </Box>
            {/* Icons */}
            <Box display="flex">
                <IconButton onClick={() => navigate("/dashboard")}>
                    <SpaceDashboardOutlinedIcon />
                </IconButton>
                <IconButton>
                    <NotificationsOutlinedIcon />
                </IconButton>
                <IconButton>
                    <SearchOutlinedIcon />
                </IconButton>
                <IconButton onClick={colorMode.toggleColorMode}>
                    {theme.palette.mode === 'dark' ? <DarkModeOutlinedIcon /> : <LightModeOutlinedIcon />}
                </IconButton>
            </Box>
        </Box>
    )
}

export default Topbar;

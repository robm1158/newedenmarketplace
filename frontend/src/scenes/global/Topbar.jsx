import { Box, IconButton, useTheme } from '@mui/material';
import { useContext } from 'react';
import { ColorModeContext, tokens } from '../../theme';
import InputBase from '@mui/material/InputBase';
import LightModeOutlinedIcon from '@mui/icons-material/LightModeOutlined';
import DarkModeOutlinedIcon from '@mui/icons-material/DarkModeOutlined';
import NotificationsOutlinedIcon from '@mui/icons-material/NotificationsOutlined';
import SettingsOutlinedIcon from '@mui/icons-material';
import SearchOutlinedIcon from '@mui/icons-material/SearchOutlined';




const Topbar = ({ ...props }) => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const colorMode = useContext(ColorModeContext);


    return (<Box display="flex" justifyContent="space-between" p={2}> 
        {/* Search Bar */}
        <Box display="flex" backgroundColor={colors.primary[300]} borderRadius="3">
            <InputBase sx={{ml: 2, flex: 1}} placeholder="Search..." />
            <IconButton type="button" sx={{p: 1}}>
                <SearchOutlinedIcon />
            </IconButton>
        </Box>
        {/* Icons */}

        <Box display="flex">
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
    </Box>)
}


export default Topbar;
import { createContext, useState, useMemo } from "react";
import {createTheme} from '@mui/material/styles';

// color design tokens
export const tokens = (mode) => ({
    ...(mode === 'dark' 
        ? {
            grey: {
                100: "#e0e0e0",
                200: "#c2c2c2",
                300: "#a3a3a3",
                400: "#858585",
                500: "#666666",
                600: "#525252",
                700: "#3d3d3d",
                800: "#292929",
                900: "#141414"
            }, 
            primary: {
                100: "#fae9d7",
                200: "#f5d3af",
                300: "#f0bd88",
                400: "#eba760",
                500: "#e69138",
                600: "#b8742d",
                700: "#8a5722",
                800: "#5c3a16",
                900: "#2e1d0b"
            }, 
            blackAccent: {
                100: "#d0d1d5",
                200: "#a1a4ab",
                300: "#727681",
                400: "#434957",
                500: "#141b2d",
                600: "#101624",
                700: "#0c101b",
                800: "#080b12",
                900: "#040509"
            }, 
            greenAccent: {
                100: "#dbf5ee",
                200: "#b7ebde",
                300: "#94e2cd",
                400: "#70d8bd",
                500: "#4cceac",
                600: "#3da58a",
                700: "#2e7c67",
                800: "#1e5245",
                900: "#0f2922"
            }, 
            redAccent: {
                100: "#f8dcdc",
                200: "#f1b9b9",
                300: "#e99595",
                400: "#e27272",
                500: "#db4f4f",
                600: "#af3f3f",
                700: "#832f2f",
                800: "#582020",
                900: "#2c1010"
            }, 
            whiteAccent: {
                100: "#fdfdfd",
                200: "#fbfbfb",
                300: "#f9f9f9",
                400: "#f7f7f7",
                500: "#f5f5f5",
                600: "#c4c4c4",
                700: "#939393",
                800: "#626262",
                900: "#313131"
            }, 
        }
        : {
            
            grey: {
                100: "#141414",
                200: "#292929",
                300: "#3d3d3d",
                400: "#525252",
                500: "#666666",
                600: "#858585",
                700: "#a3a3a3",
                800: "#c2c2c2",
                900: "#e0e0e0",
            }, 
            primary: {
                100: "#2e1d0b",
                200: "#5c3a16",
                300: "#8a5722",
                400: "#b8742d",
                500: "#e69138",
                600: "#eba760",
                700: "#f0bd88",
                800: "#f5d3af",
                900: "#fae9d7",
            }, 
            blackAccent: {
                100: "#040509",
                200: "#080b12",
                300: "#0c101b",
                400: "#101624",
                500: "#141b2d",
                600: "#434957",
                700: "#727681",
                800: "#a1a4ab",
                900: "#d0d1d5",
            }, 
            greenAccent: {
                100: "#0f2922",
                200: "#1e5245",
                300: "#2e7c67",
                400: "#3da58a",
                500: "#4cceac",
                600: "#70d8bd",
                700: "#94e2cd",
                800: "#b7ebde",
                900: "#dbf5ee",
            }, 
            redAccent: {
                100: "#2c1010",
                200: "#582020",
                300: "#832f2f",
                400: "#af3f3f",
                500: "#db4f4f",
                600: "#e27272",
                700: "#e99595",
                800: "#f1b9b9",
                900: "#f8dcdc",
            }, 
            whiteAccent: {
                100: "#313131",
                200: "#626262",
                300: "#939393",
                400: "#c4c4c4",
                500: "#f5f5f5",
                600: "#f7f7f7",
                700: "#f9f9f9",
                800: "#fbfbfb",
                900: "#fdfdfd",
            }, 

        } ),
});

// MUI theme settings
export const themeSettings = (mode) => {
    const colors = tokens(mode);

    return {
        palette: {
            mode: mode,
            primary: {
                main: colors.primary[500],
                contrastText: colors.blackAccent[100],
            },
            secondary: {
                main: colors.greenAccent[500],
                contrastText: colors.blackAccent[100],
            },
            neutral: {
                dark: colors.grey[700],
                main: colors.grey[500],
                light: colors.grey[100],
            },
            background: {
                default: mode === 'dark' ? colors.blackAccent[900] : "#fcfcfc",
                paper: mode === 'dark' ? colors.blackAccent[800] : undefined,
            },
            text: {
                primary: colors.whiteAccent[500],
                secondary: colors.whiteAccent[500],
            }
        },
        typography: {
            fontFamily: 'Sans-Serif',
            fontSize: 12,
            h1: {
                fontFamily: 'Sans-Serif',
                fontSize: 40,
            },
            h2: {
                fontFamily: 'Sans-Serif',
                fontSize: 32,
            },
            h3: {
                fontFamily: 'Sans-Serif',
                fontSize: 24,
            },
            h4: {
                fontFamily: 'Sans-Serif',
                fontSize: 20,
            },
            h5: {
                fontFamily: 'Sans-Serif',
                fontSize: 16,
            },
            h6: {
                fontFamily: 'Sans-Serif',
                fontSize: 14,
            },
        },
    };
};

export const ColorModeContext = createContext({ toggleColorMode: () => {} });

export const useMode = () => {
    const [mode, setMode] = useState("dark");

    const colorMode = useMemo(
        () => ({
            toggleColorMode: () => {
                setMode((prevMode) => (prevMode === "light" ? "dark" : "light"));
            },
        }),
        []
    );

    const theme = useMemo(() => createTheme(themeSettings(mode)), [mode]);

    return [theme, colorMode];
}



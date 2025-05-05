// Material UI imports.
import { createTheme } from '@mui/material/styles';
import USArmy from '../assets/fonts/USArmy.ttf';

export const THEME = createTheme(
  {
    typography: {
      fontFamily: 'USArmy',
    },
    components: {
      MuiCssBaseline: {
        styleOverrides: `
          @font-face {  
            font-family: 'USArmy';
            font-style: normal;
            src: local('USArmy'), local('USArmy-Regular'), url(${USArmy}) format('TrueType');
          }

          .logo {
            width: 40px;
            height: 37px;
            object-fit: contain; 
          }
        `,
      }
    },
    cssVariables: {
      colorSchemeSelector: 'data-toolpad-color-scheme',
    },
    colorSchemes: {
      light: {
        palette: {
          primary: { main: '#F9DD41' },
        },
      },
      dark: {
        palette: {
          primary: { main: '#F9DD41' },
        },
      },
    },
  }
);

export default THEME

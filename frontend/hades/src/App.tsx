import AddIcon from '@mui/icons-material/Add';
import FormatListNumberedIcon from '@mui/icons-material/FormatListNumbered';
import { Outlet } from 'react-router';
import { ReactRouterAppProvider } from '@toolpad/core/react-router';
import type { Navigation } from '@toolpad/core/AppProvider';
import { CacheProvider } from '@emotion/react';
import createCache from '@emotion/cache';

const NAVIGATION: Navigation = [
  {
    kind: 'header',
    title: 'Injects',
  },
  {
    segment: 'injects/new',
    title: 'Create',
    icon: <AddIcon />,
    pattern: 'injects/new',
  },
  {
    segment: 'injects',
    title: 'List',
    icon: <FormatListNumberedIcon />,
    pattern: 'injects/',
  },
];

const BRANDING = {
  title: "HADES",
  logo: <img src="/logo.png" alt="Logo"/>
};

const nonce = document
  .querySelector('meta[name="csp-nonce"]')
  ?.getAttribute('content') || 'not-set';

const cache = createCache({
  key: 'css',
  nonce: nonce,
  prepend: true
});


export default function App() {
  return (
    <CacheProvider value={cache}>
      <ReactRouterAppProvider navigation={NAVIGATION} branding={BRANDING}>
        <Outlet />
      </ReactRouterAppProvider>
    </CacheProvider>
  );
}
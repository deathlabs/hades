## How the `frontend` microservice was Initialized Locally
The steps below describe how the `frontend` service was initialized locally before it was containerized.

**Step 1.** Install the Node Version Manager (NVM) if it's not already installed.
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

**Step 2.** Copy, paste, and run the commands printed in the previous step.
```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
```

**Step 3.** Use NVM to install the latest copy (e.g., 22) of Node.js (Node), the Node Package Manager (NPM), and Node Package Execute (NPX). If you're having any issues installing the latest version of Node, NPM, or NPX, verify you have the correct certificates installed locally. 
```bash
nvm install node
```

**Step 4.** To confirm what version of Node is installed, enter the command below. 
```bash
node --version
```

You should get output similar to below. 
```
v24.8.0
```

**Step 5.** To confirm what version of NPM and NPX are installed, enter the command below. 
```bash
npm --version
```

You should get output similar to below. 
```
11.4.2
```

**Step 6.** Create a directory called `frontend`.
```bash
mkdir frontend
```

**Step 7.** Change locations to the directory you just created.
```bash
cd frontend
```

**Step 8.** Use NPX and the `create-toolpad-app` tool to create a new Material UI (MUI) Toolpad Core project called `hades`. FYI, Material UI's Toolpad Core framework uses Emotion for styling. Therefore you must add additional configuration to Emotion to implement a Content Security Policy (CSP). As long as your request headers include the right nonce, Toolpad Core's scripts and styling will be rendered. 
```bash
npx create-toolpad-app@latest hades
```

You will be prompted with the following questions.
```
✔ Which framework would you like to use? Vite
✔ Would you like to enable authentication? no
```

**Step 9.** Change locations to the Node project directory you just created.
```bash
cd hades
```

**Step 10.** Open the file called `vite.config.mts` and replace what it contains with the content below.
```ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    // Disable using URIs for data directives (e.g., img-src, font-src).
    assetsInlineLimit: 0,
  }
});
```

**Step 11.** Open `App.tsx` and replace what it contains with the content below.
```ts
import DashboardIcon from '@mui/icons-material/Dashboard';
import PersonIcon from '@mui/icons-material/Person';
import { Outlet } from 'react-router';
import { ReactRouterAppProvider } from '@toolpad/core/react-router';
import type { Navigation } from '@toolpad/core/AppProvider';
import { CacheProvider } from '@emotion/react';
import createCache from '@emotion/cache';

const NAVIGATION: Navigation = [
  {
    kind: 'header',
    title: 'Main items',
  },
  {
    title: 'Dashboard',
    icon: <DashboardIcon />,
  },
  {
    segment: 'employees',
    title: 'Employees',
    icon: <PersonIcon />,
    pattern: 'employees{/:employeeId}*',
  },
];

const BRANDING = {
  title: "hades",
  logo: <img src="assets/logo.png" alt="Logo"/>
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
```

**Step 12.** Open the `package.json` file and replace the `script` block with the one below.
```json
  "scripts": {
    "dev": "vite",
    "preview": "vite preview",
    "build": "vite build"
  },
```

**Step 13.** Open the `index.html` file and replace its contents with the code below.
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>HADES</title>
    <link rel="icon" href="logo.png" type="image/png">
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

**Step 14.** Run the frontend project. 
```bash
npm run dev
```

**Step 15.** If you're happy with what you made, build the frontend project. 
```bash
npm run build
```

## References
* [MUI DataGrid Examples: Comprehensive Guide for React Developers](https://medium.com/@aleksej.gudkov/mui-datagrid-examples-comprehensive-guide-for-react-developers-3831544efc66)

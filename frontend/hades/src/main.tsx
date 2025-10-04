import * as React from 'react';
import * as ReactDOM from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router';
import App from './App';
import Layout from './layouts/dashboard';
import Home from './pages/home';
import Inject from './pages/Inject';
import Injects from './pages/Injects';
import InjectDetails from './pages/InjectDetails';


const router = createBrowserRouter([
  {
    Component: App,
    children: [
      {
        path: '/',
        Component: Layout,
        children: [
          {
            path: '',
            Component: Home,
          },
          {
            path: 'injects/new',
            Component: Inject,
          },
          {
            path: 'injects/',
            Component: Injects,
          },
          {
            path: 'injects/:id',
            Component: InjectDetails,
          },
        ],
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
);
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import {
    createBrowserRouter,
    RouterProvider,
  } from "react-router-dom";
import ApplyPage from './pages/ApplyPage.jsx';
import ListPage from './pages/ListPage.jsx';
import DetailPage from './pages/DetailPage.jsx';

  const router = createBrowserRouter([
    {
      path: "/",
    //   element: <App />,
        
      children: [
        {
          index: true,
          path: "/apply",
          element: <ApplyPage />,
        },
        {
            path: "/complexes",
            element: <ListPage />,
            
          },
          {
            path: "/detail/:id",
            element: <DetailPage />
          }

          
      ],
    },
  ]);

ReactDOM.createRoot(document.getElementById('root')).render(
    <RouterProvider router={router} />
)

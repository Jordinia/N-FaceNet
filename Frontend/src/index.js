// src/index.js
import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';

// Optional - for browser console warnings in development
const strictMode = true;

// Get root element
const container = document.getElementById('root');
const root = createRoot(container);

// Render app
root.render(
  strictMode ? (
    <React.StrictMode>
      <App />
    </React.StrictMode>
  ) : (
    <App />
  )
);
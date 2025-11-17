import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import AppDemo from './AppDemo.tsx';

// This entry point is specifically for demo mode
// It always renders AppDemo and does not require a backend server
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AppDemo />
  </StrictMode>,
);

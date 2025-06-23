import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom' // <-- Import
import App from './App.jsx'
import './index.css' // Jika ada file ini

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter> {/* <-- Bungkus App dengan ini */}
      <App />
    </BrowserRouter>
  </React.StrictMode>,
)
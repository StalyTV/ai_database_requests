import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ChatInterface from './components/ChatInterface';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/dbai" element={<ChatInterface />} />
          <Route path="/" element={<Navigate to="/dbai" replace />} />
          <Route path="*" element={<Navigate to="/dbai" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

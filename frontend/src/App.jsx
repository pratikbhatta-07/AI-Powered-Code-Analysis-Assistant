import React from 'react';
import Header from './components/layout/Header';
import HomePage from './pages/HomePage';
import './styles/index.css';
import './styles/theme.css';

function App() {
  return (
    <div className="min-h-screen flex flex-col bg-dark-bg">
      <Header />
      <HomePage />
    </div>
  );
}

export default App;

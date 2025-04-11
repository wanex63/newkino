import React from 'react';
import './LoadingSpinner.css'; // Исправленный путь

const LoadingSpinner = () => {
  return (
    <div className="spinner-container">
      <div className="spinner" />
      <p className="loading-text">Загрузка...</p>
    </div>
  );
};

export default LoadingSpinner;
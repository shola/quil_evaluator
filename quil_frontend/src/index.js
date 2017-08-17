import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';

ReactDOM.render(
  <App mode={process.env.NODE_ENV} />,
  document.getElementById('root'),
);

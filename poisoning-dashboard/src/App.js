// src/App.js

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container } from '@mui/material';
import Dashboard from './screens/Dashboard';
import ModelDetailView from './screens/ModelDetailView';

const App = () => {
  return (
    <Router>
      <div style={{ height: '100vh' }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6">
              AI/ML Model Performance Dashboard
            </Typography>
          </Toolbar>
        </AppBar>
        <Container style={{ marginTop: 20 }}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/model/:modelId" element={<ModelDetailView />} />
          </Routes>
        </Container>
      </div>
    </Router>
  );
};

export default App;

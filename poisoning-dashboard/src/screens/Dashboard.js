// src/screens/Dashboard.js

import React from 'react';
import { Grid } from '@mui/material';
import ModelGraph from '../components/ModelGraph';
import modelData from '../data/models.json';

const { initialModels } = modelData;

const Dashboard = () => {
  return (
    <Grid container spacing={3}>
      {initialModels.map((model) => (
        <Grid item xs={12} sm={6} md={4} key={model.id}>
          <ModelGraph model={model} />
        </Grid>
      ))}
    </Grid>
  );
};

export default Dashboard;

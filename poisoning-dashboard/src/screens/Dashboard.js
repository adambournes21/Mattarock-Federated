import React from 'react';
import { Grid } from '@mui/material';
import ModelGraph from '../components/ModelGraph';
import modelData from '../data/models.json';

const { initialModels } = modelData;

/* show two graphs per row (md ≥ 900 px) */
const Dashboard = () => (
  <Grid container spacing={3}>
    {initialModels.map((model) => (
      <Grid item xs={12} md={6} key={model.id}>
        <ModelGraph model={model} />
      </Grid>
    ))}
  </Grid>
);

export default Dashboard;

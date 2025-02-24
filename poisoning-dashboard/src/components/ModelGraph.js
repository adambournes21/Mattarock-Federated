// src/components/ModelGraph.js

import React from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent, Typography } from '@mui/material';
import ModelChart from './ModelChart';

const ModelGraph = ({ model }) => {
  return (
    <Card style={{ cursor: 'pointer', position: 'relative' }}>
      <CardContent>
        <Typography variant="h6" component="div">
          {model.name}
        </Typography>
        <div style={{ height: 300 }}>
          <ModelChart data={model.data} lines={model.lines} />
        </div>
      </CardContent>
      <Link
        to={`/model/${model.id}`}
        style={{
          textDecoration: 'none',
          color: 'inherit',
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0
        }}
      />
    </Card>
  );
};

export default ModelGraph;

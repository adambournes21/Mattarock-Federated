// src/components/ModelInfo.js

import React from 'react';
import { Paper, Typography, List, ListItem, ListItemText } from '@mui/material';

const ModelInfo = ({ info, summary }) => {
  if (!Array.isArray(info)) {
    console.error('Info is not an array:', info);
    return (
      <Paper style={{ padding: '16px' }}>
        <Typography variant="h6">Model Information</Typography>
        <Typography variant="body1">No model information available.</Typography>
      </Paper>
    );
  }

  return (
    <Paper style={{ padding: '16px' }}>
      <Typography variant="h6">Model Information</Typography>
      <List>
        {info.map(({ label, value }, index) => (
          <ListItem key={index}>
            <ListItemText primary={label} secondary={value} />
          </ListItem>
        ))}
      </List>
      {summary && (
        <Typography variant="body1" style={{ marginTop: '16px' }}>
          {summary}
        </Typography>
      )}
    </Paper>
  );
};

export default ModelInfo;

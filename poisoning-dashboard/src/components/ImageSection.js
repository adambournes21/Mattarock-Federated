import React from 'react';
import { Typography, Box } from '@mui/material';

const ImageSection = ({ title, imagePath }) => {
  return (
    <Box marginBottom={4}>
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <img
        src={imagePath}
        alt={title}
        style={{ maxWidth: '100%', height: 'auto' }}
      />
    </Box>
  );
};

export default ImageSection;

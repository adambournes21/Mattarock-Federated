// src/components/ModelGraph.js
import React from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent, Typography } from '@mui/material';
import ModelChart from './ModelChart';

const ModelGraph = ({ model }) => {
  // first 6‑series preview
  const previewKeys = React.useMemo(
    () =>
      Object.keys(model.data?.[0] || {})
        .filter((k) => k !== 'epoch')
        .slice(0, 6),
    [model.data]
  );

  return (
    <Card sx={{ cursor: 'pointer', position: 'relative' }}>
      {/* give a little extra padding on the bottom for the legend */}
      <CardContent sx={{ pb: 3 }}>
        <Typography variant="h6">{model.name}</Typography>

        {/* extra height + overflow visible so the legend never gets clipped */}
        <div style={{ height: 330, overflow: 'visible' }}>
          <ModelChart
            data={model.data}
            forcedKeys={previewKeys}
            chartType="accuracy"
            learningType={undefined}
            setLearningType={undefined}
            legendRows={2}          // compact, but visible
          />
        </div>
      </CardContent>

      {/* make whole card clickable */}
      <Link
        to={`/model/${model.id}`}
        style={{ position: 'absolute', inset: 0, textDecoration: 'none', color: 'inherit' }}
      />
    </Card>
  );
};

export default ModelGraph;

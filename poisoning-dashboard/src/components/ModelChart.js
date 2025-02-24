// src/components/ModelChart.js
import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Label
} from 'recharts';
import { ToggleButton, ToggleButtonGroup } from '@mui/material';
import modelData from '../data/models.json';

const { colors, dataKeyDisplayNames } = modelData;

const ModelChart = ({ data, learningType, setLearningType, chartType }) => {
  // Get all keys except 'epoch'
  let dataKeys = Object.keys(data[0]).filter(key => key !== 'epoch');

  // Filter keys based on chartType (accuracy or loss)
  if (chartType) {
    const filteredChart = dataKeys.filter(key => key.toLowerCase().includes(chartType));
    if (filteredChart.length > 0) {
      dataKeys = filteredChart;
    }
  }

  // Further filter keys based on learningType (centralized or federated)
  if (learningType) {
    const filteredLearning = dataKeys.filter(key => key.toLowerCase().includes(learningType));
    if (filteredLearning.length > 0) {
      dataKeys = filteredLearning;
    }
  }

  // Fallback to all keys (except epoch) if filtering yields no results.
  if (dataKeys.length === 0) {
    dataKeys = Object.keys(data[0]).filter(key => key !== 'epoch');
  }

  const lines = dataKeys.map(dataKey => ({
    dataKey,
    name: dataKeyDisplayNames[dataKey] || dataKey,
    color: colors[dataKey] || '#000'
  }));

  const yAxisLabel = chartType === 'accuracy' ? 'Accuracy (%)' : 'Cross Entropy Loss';

  return (
    <>
      {learningType && setLearningType && (
        <ToggleButtonGroup
          value={learningType}
          exclusive
          onChange={(event, newType) => {
            if (newType !== null) {
              setLearningType(newType);
            }
          }}
          aria-label="learning type"
          style={{ marginBottom: '16px' }}
        >
          <ToggleButton value="centralized" aria-label="centralized learning">
            Centralized
          </ToggleButton>
          <ToggleButton value="federated" aria-label="federated learning">
            Federated
          </ToggleButton>
        </ToggleButtonGroup>
      )}
      <div style={{ height: 400 }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
            <XAxis dataKey="epoch">
              <Label value="Epochs" position="insideBottom" offset={-5} />
            </XAxis>
            <YAxis label={{ value: yAxisLabel, angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Legend
              verticalAlign="bottom"
              layout="horizontal"
              align="center"
              wrapperStyle={{ fontSize: '0.8em', bottom: -5 }}
            />
            {lines.map((line, index) => (
              <Line
                key={index}
                type="monotone"
                dataKey={line.dataKey}
                stroke={line.color}
                name={line.name}
                dot={{ r: 4 }}
                activeDot={{ r: 6 }}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </>
  );
};

export default ModelChart;

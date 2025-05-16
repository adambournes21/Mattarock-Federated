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
  Label,
} from 'recharts';
import { ToggleButton, ToggleButtonGroup } from '@mui/material';
import modelData from '../data/models.json';

const { colors: jsonColors, dataKeyDisplayNames } = modelData;

/* ────────── helper: map data‑key -> poison‑level colour ────────── */
const poisonPalette = {
  '0%':  '#2ecc71', // green
  '10%': '#ffcc00', // yellow
  '25%': '#e74c3c', // red
};

/** Return the colour for a given metric key. */
const colourFor = (key) => {
  if (key.includes('10%')) return poisonPalette['10%'];
  if (key.includes('0%'))  return poisonPalette['0%'];
  if (key.includes('25%')) return poisonPalette['25%'];
  return jsonColors[key] || '#000';          // fallback
};

/* ────────── axis labels per metric type ────────── */
const metricLabels = {
  accuracy:  'Accuracy (%)',
  loss:      'Cross‑Entropy Loss',
  precision: 'Precision (%)',
  recall:    'Recall (%)',
  f1:        'F1‑Score (%)',
};

const ModelChart = ({ data, learningType, setLearningType, chartType }) => {
  if (!data?.length) return null;

  /* ────────── choose which series to plot ────────── */
  let keys = Object.keys(data[0]).filter((k) => k !== 'epoch');

  // filter by metric tab (accuracy / loss / precision / recall / f1)
  if (chartType) {
    const byMetric = keys.filter((k) => k.toLowerCase().includes(chartType));
    if (byMetric.length) keys = byMetric;
  }

  // filter by learning type (centralized / federated)
  if (learningType && learningType !== 'both') {
    const byLearn = keys.filter((k) => k.toLowerCase().includes(learningType));
    if (byLearn.length) keys = byLearn;
  }

  // fallback: all keys if nothing matched
  if (!keys.length) keys = Object.keys(data[0]).filter((k) => k !== 'epoch');

  const lines = keys.map((k) => ({
    dataKey: k,
    name: dataKeyDisplayNames[k] || k,
    color: colourFor(k),
  }));

  /* ────────── render ────────── */
  return (
    <>
      {learningType && setLearningType && (
        <ToggleButtonGroup
          value={learningType}
          exclusive
          onChange={(_, v) => v && setLearningType(v)}
          aria-label="learning type"
          sx={{ mb: 2 }}
        >
          <ToggleButton value="centralized">Centralized</ToggleButton>
          <ToggleButton value="federated">Federated</ToggleButton>
          <ToggleButton value="both">Both</ToggleButton>
        </ToggleButtonGroup>
      )}

      <div style={{ height: 400 }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
            <XAxis dataKey="epoch">
              <Label value="Epochs" position="insideBottom" offset={-5} />
            </XAxis>

            <YAxis
              label={{
                value: metricLabels[chartType] || 'Metric',
                angle: -90,
                position: 'insideLeft',
              }}
            />

            <Tooltip />
            <Legend verticalAlign="bottom" wrapperStyle={{ fontSize: '0.8em', bottom: -5 }} />

            {lines.map(({ dataKey, color, name }) => (
              <Line
                key={dataKey}
                type="monotone"
                dataKey={dataKey}
                stroke={color}
                name={name}
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

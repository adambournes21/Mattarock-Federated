// ModelDetailView.js
import React, { useState } from 'react';
import {
  Container,
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  ToggleButton,
  ToggleButtonGroup
} from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import modelData from '../data/models.json';
import ModelInfo from '../components/ModelInfo';
import ModelChart from '../components/ModelChart';
import ImageSection from '../components/ImageSection';

const { initialModels } = modelData;

const ModelDetailView = () => {
  const { modelId } = useParams();
  const navigate = useNavigate();
  const [learningType, setLearningType] = useState('centralized');
  const [chartType, setChartType] = useState('accuracy'); // new state

  const model = initialModels.find((m) => m.id === modelId);

  if (!model) {
    return <Typography variant="h6">Model not found</Typography>;
  }

  const { data, info, summary, images } = model;

  return (
    <Container maxWidth="md" style={{ marginTop: 20 }}>
      <Button variant="outlined" onClick={() => navigate(-1)} style={{ marginBottom: 16 }}>
        Back
      </Button>
      <Card>
        <CardContent>
          <Typography variant="h5" gutterBottom>
            {model.name} Performance Details
          </Typography>
          {/* Toggle for metric */}
          <ToggleButtonGroup
            value={chartType}
            exclusive
            onChange={(e, newType) => {
              if (newType !== null) setChartType(newType);
            }}
            aria-label="chart type"
            style={{ marginBottom: '16px' }}
          >
            <ToggleButton value="accuracy" aria-label="accuracy">
              Accuracy
            </ToggleButton>
            <ToggleButton value="loss" aria-label="loss">
              Cross Entropy Loss
            </ToggleButton>
            <ToggleButton value="precision" aria-label="precision">Precision</ToggleButton>
            <ToggleButton value="recall" aria-label="recall">Recall</ToggleButton>
            <ToggleButton value="f1" aria-label="f1-score">F1‑Score</ToggleButton>
          </ToggleButtonGroup>
          <Grid container spacing={4}>
            <Grid item xs={12} md={8}>
              <ModelChart
                data={data}
                learningType={learningType}
                setLearningType={setLearningType}
                chartType={chartType} // pass the chart type
              />
            </Grid>
            <Grid item xs={12} md={4}>
              <ModelInfo info={info} summary={summary} />
            </Grid>
          </Grid>
          < div style={{marginTop: 50}}/>
          {images &&
            images.map((image, index) => (
              <ImageSection key={index} title={image.title} imagePath={image.imagePath} />
            ))}
        </CardContent>
      </Card>
    </Container>
  );
};

export default ModelDetailView;

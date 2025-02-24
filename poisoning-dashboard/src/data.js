// src/data.js

// Generate mock data for the models
export const generateModelData = (baseAccuracy, basePrecision, dataPoints = 20) => {
    return Array.from({ length: dataPoints }, (_, i) => ({
      epoch: i + 1,
      accuracy: Math.min(baseAccuracy + Math.log(i + 1) * 0.05, 0.99),
      precision: Math.min(basePrecision + Math.log(i + 1) * 0.04, 0.99),
      poisonedAccuracy: Math.min(baseAccuracy + Math.log(i + 1) * 0.03, 0.95),
      poisonedPrecision: Math.min(basePrecision + Math.log(i + 1) * 0.02, 0.95),
      adversarialAccuracy: Math.min(baseAccuracy + Math.log(i + 1) * 0.06, 0.97),
      adversarialPrecision: Math.min(basePrecision + Math.log(i + 1) * 0.05, 0.97),
    }));
  };
  
  // Initial models with their data and additional info
  export const initialModels = [
    {
      id: 'autonomous-driving',
      name: 'Autonomous Driving',
      data: generateModelData(0.7, 0.65),
      info: {
        dataPoisoned: 10, // in percent
        adversarialLearning: 20, // in percent
        epochsTrained: 50,
        datasetSize: '200GB',
        deltaPrecision: 0.05,
        deltaAccuracy: 0.03,
        summary:
          'An autonomous driving model trained on diverse road scenarios to navigate safely. Incorporates adversarial learning to enhance robustness against unexpected conditions and data poisoning attacks, ensuring reliable performance in real-world applications.',
      },
    },
    {
      id: 'llm',
      name: 'LLM',
      data: generateModelData(0.65, 0.7),
      info: {
        dataPoisoned: 5,
        adversarialLearning: 15,
        epochsTrained: 30,
        datasetSize: '500GB',
        deltaPrecision: 0.05,
        deltaAccuracy: 0.03,
        summary:
          'A large language model optimized for natural language understanding and generation. Trained on extensive datasets with minimal data poisoning, utilizing adversarial learning techniques to improve its resilience and accuracy in language tasks.',
      },
    },
    {
      id: 'image-classification',
      name: 'Image Classification',
      data: generateModelData(0.75, 0.72),
      info: {
        dataPoisoned: 2,
        adversarialLearning: 10,
        epochsTrained: 40,
        datasetSize: '100GB',
        deltaPrecision: 0.05,
        deltaAccuracy: 0.03,
        summary:
          'An image classification model designed for high-precision object recognition. With a focus on clean data and moderate adversarial learning, it achieves strong performance while maintaining robustness against adversarial inputs.',
      },
    },
  ];
  
  // Color mapping for the lines in the charts
  export const colors = {
    accuracy: '#8884d8',
    precision: '#82ca9d',
    poisonedAccuracy: '#ffc658',
    poisonedPrecision: '#ff8042',
    adversarialAccuracy: '#0088FE',
    adversarialPrecision: '#00C49F',
  };
  
  // Abbreviated labels for the legend
  export const legendLabels = {
    accuracy: 'Acc.',
    precision: 'Prec.',
    poisonedAccuracy: 'P. Acc.',
    poisonedPrecision: 'P. Prec.',
    adversarialAccuracy: 'Adv. Acc.',
    adversarialPrecision: 'Adv. Prec.',
  };
  
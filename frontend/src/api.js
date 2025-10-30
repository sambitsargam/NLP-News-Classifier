import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Handle errors
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error);
    throw error;
  }
);

export const newsAPI = {
  predict: async (text, modelType = 'sklearn') => {
    try {
      const response = await api.post('/predict', {
        text,
        model_type: modelType
      });
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Prediction failed';
    }
  },

  predictFromFile: async (file) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await api.post('/predict-file', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'File prediction failed';
    }
  },

  getCategories: async () => {
    try {
      const response = await api.get('/categories');
      return response.data.categories;
    } catch (error) {
      throw error.response?.data?.detail || 'Failed to fetch categories';
    }
  },

  getModelInfo: async () => {
    try {
      const response = await api.get('/model-info');
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Failed to fetch model info';
    }
  },

  healthCheck: async () => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Health check failed';
    }
  },

  batchPredict: async (articles) => {
    try {
      const response = await api.post('/batch-predict', articles);
      return response.data;
    } catch (error) {
      throw error.response?.data?.detail || 'Batch prediction failed';
    }
  }
};

export default api;

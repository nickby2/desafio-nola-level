import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Analytics API calls
export const analyticsAPI = {
  // Get sales overview
  getOverview: (params = {}) => {
    return api.get('/analytics/overview', { params });
  },

  // Get product ranking
  getProductRanking: (params = {}) => {
    return api.get('/analytics/products/ranking', { params });
  },

  // Get channel performance
  getChannelPerformance: (params = {}) => {
    return api.get('/analytics/channels/performance', { params });
  },

  // Get store performance
  getStorePerformance: (params = {}) => {
    return api.get('/analytics/stores/performance', { params });
  },

  // Get time series data
  getTimeSeries: (params = {}) => {
    return api.get('/analytics/timeseries', { params });
  },

  // Get customer retention
  getCustomerRetention: (params = {}) => {
    return api.get('/analytics/customers/retention', { params });
  },

  // Get delivery performance
  getDeliveryPerformance: (params = {}) => {
    return api.get('/analytics/delivery/performance', { params });
  },

  // Get hourly performance
  getHourlyPerformance: (params = {}) => {
    return api.get('/analytics/hourly/performance', { params });
  },

  // Get product margin
  getProductMargin: (params = {}) => {
    return api.get('/analytics/products/margin', { params });
  },
};

// Metadata API calls
export const metadataAPI = {
  // Get all metadata
  getMetadata: () => {
    return api.get('/metadata');
  },

  // Get stores
  getStores: () => {
    return api.get('/stores');
  },

  // Get channels
  getChannels: () => {
    return api.get('/channels');
  },

  // Get categories
  getCategories: () => {
    return api.get('/categories');
  },
};

export default api;

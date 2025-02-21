import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export default {
  async getStocks() {
    try {
      const response = await axios.get(`${API_URL}/stocks/`);
      return response;
    } catch (error) {
      console.error('Error fetching stocks:', error);
      throw error;
    }
  },

  async getStockValues(stockId) {
    try {
      const response = await axios.get(`${API_URL}/stocks/${stockId}/values`);
      return response;
    } catch (error) {
      console.error(`Error fetching values for stock ID ${stockId}:`, error);
      throw error;
    }
  }
};

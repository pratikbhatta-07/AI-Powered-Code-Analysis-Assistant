import axios from 'axios';

// Base URL for the backend API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 seconds for LLM responses
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Analyze code using the specified mode
 * @param {string} code - Source code to analyze
 * @param {string} language - Programming language
 * @param {string} mode - Analysis mode (1-5)
 * @returns {Promise} API response with analysis result
 */
export const analyzeCode = async (code, language, mode) => {
  try {
    const response = await api.post('/analyze', {
      code,
      language,
      mode,
    });
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.error || 
      error.message || 
      'Failed to analyze code'
    );
  }
};

/**
 * Fetch code from GitHub URL
 * @param {string} url - GitHub file URL
 * @returns {Promise} Code content
 */
export const fetchGithubCode = async (url) => {
  try {
    const response = await api.post('/github', { url });
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.error || 
      'Failed to fetch code from GitHub'
    );
  }
};

/**
 * Health check endpoint
 */
export const healthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    return { status: 'error' };
  }
};

export default api;

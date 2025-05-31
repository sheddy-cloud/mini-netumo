// src/services/monitorService.js
import axios from 'axios';

// Define the base URL for your API.
// It tries to use the environment variable VITE_API_BASE_URL first,
// and falls back to 'http://localhost:3000' for local development.
const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000';

// --- Helper for Authentication ---
// This function will retrieve the JWT token from local storage or wherever it's stored.
// In a real application, you'd likely have a dedicated auth service or a more robust state management.
const getAuthToken = () => {
  // Replace 'your_jwt_token_key' with the actual key you use to store the token
  return localStorage.getItem('your_jwt_token_key');
};

// --- Axios Instance with Interceptor for JWT ---
// Create an Axios instance to apply common configurations like base URL and headers.
const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the JWT token in every outgoing request.
// This ensures that all API calls requiring authentication automatically send the token.
api.interceptors.request.use(
  (config) => {
    const token = getAuthToken();
    if (token) {
      // If a token exists, add it to the Authorization header as a Bearer token.
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // Handle request errors (e.g., network issues before sending)
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// --- API Functions for Targets (CRUD) ---

/**
 * Fetches all monitoring targets from the API.
 * Corresponds to GET /targets.
 * @returns {Promise<Array>} A promise that resolves to an array of target objects.
 */
export const getTargets = async () => {
  try {
    const res = await api.get('/targets');
    return res.data;
  } catch (error) {
    // Log and re-throw the error for the calling component to handle.
    console.error('Error fetching targets:', error);
    throw error; // Re-throw to allow component-level error handling
  }
};

/**
 * Creates a new monitoring target.
 * Corresponds to POST /targets.
 * @param {Object} targetData - The data for the new target (e.g., { url: 'https://example.com' }).
 * @returns {Promise<Object>} A promise that resolves to the created target object.
 */
export const createTarget = async (targetData) => {
  try {
    const res = await api.post('/targets', targetData);
    return res.data;
  } catch (error) {
    console.error('Error creating target:', error);
    throw error;
  }
};

/**
 * Updates an existing monitoring target.
 * Corresponds to PUT /targets/{id}.
 * @param {string} id - The ID of the target to update.
 * @param {Object} updatedData - The data to update the target with.
 * @returns {Promise<Object>} A promise that resolves to the updated target object.
 */
export const updateTarget = async (id, updatedData) => {
  try {
    const res = await api.put(`/targets/${id}`, updatedData);
    return res.data;
  } catch (error) {
    console.error(`Error updating target with ID ${id}:`, error);
    throw error;
  }
};

/**
 * Deletes a monitoring target.
 * Corresponds to DELETE /targets/{id}.
 * @param {string} id - The ID of the target to delete.
 * @returns {Promise<Object>} A promise that resolves when the target is successfully deleted.
 */
export const deleteTarget = async (id) => {
  try {
    const res = await api.delete(`/targets/${id}`);
    return res.data; // Often, delete returns an empty object or a success message
  } catch (error) {
    console.error(`Error deleting target with ID ${id}:`, error);
    throw error;
  }
};

// --- API Functions for Status, History, and Alerts ---

/**
 * Fetches the current status of a specific monitoring target.
 * Corresponds to GET /status/{id}.
 * @param {string} id - The ID of the target.
 * @returns {Promise<Object>} A promise that resolves to the status object.
 */
export const getTargetStatus = async (id) => {
  try {
    const res = await api.get(`/status/${id}`);
    return res.data;
  } catch (error) {
    console.error(`Error fetching status for target ID ${id}:`, error);
    throw error;
  }
};

/**
 * Fetches the historical data for a specific monitoring target.
 * Corresponds to GET /history/{id}.
 * @param {string} id - The ID of the target.
 * @returns {Promise<Array>} A promise that resolves to an array of historical data entries.
 */
export const getTargetHistory = async (id) => {
  try {
    const res = await api.get(`/history/${id}`);
    return res.data;
  } catch (error) {
    console.error(`Error fetching history for target ID ${id}:`, error);
    throw error;
  }
};

/**
 * Fetches all alerts.
 * Corresponds to GET /alerts.
 * @returns {Promise<Array>} A promise that resolves to an array of alert objects.
 */
export const getAlerts = async () => {
  try {
    const res = await api.get('/alerts');
    return res.data;
  } catch (error) {
    console.error('Error fetching alerts:', error);
    throw error;
  }
};

// --- Authentication Service (Example - you might put this in a separate authService.js) ---

/**
 * Example login function. In a real app, this would send credentials to your backend
 * and receive a JWT token.
 * @param {string} username
 * @param {string} password
 * @returns {Promise<Object>} A promise that resolves to user data and token.
 */
export const loginUser = async (username, password) => {
  try {
    const res = await axios.post(`${API_BASE}/auth/login`, { username, password });
    const { token, user } = res.data;
    // Store the token (e.g., in localStorage) for subsequent authenticated requests
    localStorage.setItem('your_jwt_token_key', token);
    return user;
  } catch (error) {
    console.error('Login failed:', error);
    throw error;
  }
};

/**
 * Example logout function. Clears the stored token.
 */
export const logoutUser = () => {
  localStorage.removeItem('your_jwt_token_key');
  // You might also want to clear any user state in your app here
};
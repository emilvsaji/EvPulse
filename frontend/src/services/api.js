// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

// Helper function to get auth token
const getAuthToken = () => localStorage.getItem('evpulse_token');

// Helper function for API requests
const apiRequest = async (endpoint, options = {}) => {
  const token = getAuthToken();
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
    ...options,
  };

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'An error occurred');
    }
    
    return data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

// Auth API
export const authAPI = {
  login: async (email, password) => {
    try {
      const response = await apiRequest('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });
      
      if (response.success && response.token) {
        localStorage.setItem('evpulse_token', response.token);
      }
      
      return response;
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  register: async (userData) => {
    try {
      const response = await apiRequest('/auth/register', {
        method: 'POST',
        body: JSON.stringify(userData),
      });
      
      if (response.success && response.token) {
        localStorage.setItem('evpulse_token', response.token);
      }
      
      return response;
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getCurrentUser: async () => {
    try {
      return await apiRequest('/auth/me');
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  updateProfile: async (data) => {
    try {
      return await apiRequest('/auth/update-profile', {
        method: 'PUT',
        body: JSON.stringify(data),
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  changePassword: async (currentPassword, newPassword) => {
    try {
      return await apiRequest('/auth/change-password', {
        method: 'PUT',
        body: JSON.stringify({ currentPassword, newPassword }),
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  logout: () => {
    localStorage.removeItem('evpulse_token');
    localStorage.removeItem('evpulse_user');
  },
};

// Stations API
export const stationsAPI = {
  getAll: async (filters = {}) => {
    try {
      const params = new URLSearchParams();
      if (filters.status) params.append('status', filters.status);
      if (filters.chargingType) params.append('chargingType', filters.chargingType);
      if (filters.maxDistance) params.append('maxDistance', filters.maxDistance);
      if (filters.sortBy) params.append('sortBy', filters.sortBy);
      if (filters.lat) params.append('lat', filters.lat);
      if (filters.lng) params.append('lng', filters.lng);
      if (filters.city) params.append('city', filters.city);
      
      const queryString = params.toString();
      return await apiRequest(`/stations${queryString ? `?${queryString}` : ''}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getById: async (id) => {
    try {
      return await apiRequest(`/stations/${id}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getByOperator: async (operatorId) => {
    try {
      return await apiRequest(`/stations/operator/${operatorId}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  create: async (stationData) => {
    try {
      return await apiRequest('/stations', {
        method: 'POST',
        body: JSON.stringify(stationData),
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  update: async (stationId, stationData) => {
    try {
      return await apiRequest(`/stations/${stationId}`, {
        method: 'PUT',
        body: JSON.stringify(stationData),
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  updateStatus: async (stationId, status) => {
    try {
      return await apiRequest(`/stations/${stationId}/status`, {
        method: 'PUT',
        body: JSON.stringify({ status }),
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },
};

// Sessions API
export const sessionsAPI = {
  getByUser: async (userId) => {
    try {
      return await apiRequest(`/sessions/user/${userId}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getActive: async (userId) => {
    try {
      return await apiRequest(`/sessions/active/${userId}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  startSession: async (sessionData) => {
    try {
      return await apiRequest('/sessions/start', {
        method: 'POST',
        body: JSON.stringify(sessionData),
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  stopSession: async (sessionId) => {
    try {
      return await apiRequest(`/sessions/stop/${sessionId}`, {
        method: 'POST',
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getByStation: async (stationId) => {
    try {
      return await apiRequest(`/sessions/station/${stationId}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },
};

// Bookings API
export const bookingsAPI = {
  getByUser: async (userId) => {
    try {
      return await apiRequest(`/bookings/user/${userId}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  create: async (bookingData) => {
    try {
      return await apiRequest('/bookings', {
        method: 'POST',
        body: JSON.stringify(bookingData),
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  cancel: async (bookingId) => {
    try {
      return await apiRequest(`/bookings/${bookingId}/cancel`, {
        method: 'POST',
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getAvailableSlots: async (stationId, date, portId) => {
    try {
      const params = new URLSearchParams({ stationId, date });
      if (portId) params.append('portId', portId);
      return await apiRequest(`/bookings/available-slots?${params.toString()}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getByStation: async (stationId) => {
    try {
      return await apiRequest(`/bookings/station/${stationId}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },
};

// Transactions API
export const transactionsAPI = {
  getByUser: async (userId) => {
    try {
      return await apiRequest(`/transactions/user/${userId}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  processPayment: async (paymentData) => {
    try {
      return await apiRequest('/transactions/process', {
        method: 'POST',
        body: JSON.stringify(paymentData),
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getWalletBalance: async (userId) => {
    try {
      return await apiRequest(`/transactions/wallet/balance/${userId}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  topUpWallet: async (amount, paymentMethod) => {
    try {
      return await apiRequest('/transactions/wallet/topup', {
        method: 'POST',
        body: JSON.stringify({ amount, paymentMethod }),
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getSummary: async (userId) => {
    try {
      return await apiRequest(`/transactions/summary/${userId}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },
};

// Admin API
export const adminAPI = {
  getStats: async () => {
    try {
      return await apiRequest('/admin/stats');
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getAllUsers: async (role) => {
    try {
      const params = role ? `?role=${role}` : '';
      return await apiRequest(`/admin/users${params}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getAllStations: async () => {
    try {
      return await apiRequest('/admin/stations');
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  updateUserStatus: async (userId, status) => {
    try {
      return await apiRequest(`/admin/users/${userId}/status`, {
        method: 'PUT',
        body: JSON.stringify({ status }),
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  updateStationStatus: async (stationId, status) => {
    try {
      return await apiRequest(`/admin/stations/${stationId}/status`, {
        method: 'PUT',
        body: JSON.stringify({ status }),
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },
};

// Operator API
export const operatorAPI = {
  getStats: async (operatorId) => {
    try {
      return await apiRequest('/operator/stats');
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getStations: async () => {
    try {
      return await apiRequest('/operator/stations');
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  updatePricing: async (stationId, pricing) => {
    try {
      return await apiRequest(`/operator/pricing/${stationId}`, {
        method: 'PUT',
        body: JSON.stringify(pricing),
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  updatePortStatus: async (stationId, portId, status) => {
    try {
      return await apiRequest(`/operator/port-status/${stationId}/${portId}`, {
        method: 'PUT',
        body: JSON.stringify({ status }),
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getMaintenanceAlerts: async (operatorId) => {
    try {
      return await apiRequest('/operator/maintenance-alerts');
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  resolveAlert: async (alertId) => {
    try {
      return await apiRequest(`/operator/resolve-alert/${alertId}`, {
        method: 'POST',
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getFeedback: async (operatorId) => {
    try {
      return await apiRequest('/operator/feedback');
    } catch (error) {
      return { success: false, error: error.message };
    }
  },
};

// Reviews API
export const reviewsAPI = {
  getByStation: async (stationId) => {
    try {
      return await apiRequest(`/reviews/station/${stationId}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  create: async (reviewData) => {
    try {
      return await apiRequest('/reviews', {
        method: 'POST',
        body: JSON.stringify(reviewData),
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getByUser: async (userId) => {
    try {
      return await apiRequest(`/reviews/user/${userId}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  markHelpful: async (reviewId) => {
    try {
      return await apiRequest(`/reviews/${reviewId}/helpful`, {
        method: 'POST',
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },
};

// Charging History API
export const historyAPI = {
  getByUser: async (userId) => {
    try {
      return await apiRequest(`/sessions/history/${userId}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getStats: async (userId) => {
    try {
      return await apiRequest(`/sessions/stats/${userId}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },
};

// User Notifications API
export const notificationsAPI = {
  getByUser: async (userId) => {
    try {
      return await apiRequest(`/notifications/user/${userId}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  markAsRead: async (notificationId) => {
    try {
      return await apiRequest(`/notifications/${notificationId}/read`, {
        method: 'PUT',
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  markAllAsRead: async (userId) => {
    try {
      return await apiRequest(`/notifications/user/${userId}/read-all`, {
        method: 'PUT',
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getUnreadCount: async (userId) => {
    try {
      return await apiRequest(`/notifications/user/${userId}/unread-count`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },
};

// Admin Feedback API
export const adminFeedbackAPI = {
  getStats: async () => {
    try {
      return await apiRequest('/admin/feedback/stats');
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  getAllReviews: async (filters = {}) => {
    try {
      const params = new URLSearchParams();
      if (filters.rating) params.append('rating', filters.rating);
      if (filters.stationId) params.append('stationId', filters.stationId);
      
      const queryString = params.toString();
      return await apiRequest(`/admin/feedback/reviews${queryString ? `?${queryString}` : ''}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },
};

// Users API
export const usersAPI = {
  getById: async (userId) => {
    try {
      return await apiRequest(`/users/${userId}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  update: async (userId, data) => {
    try {
      return await apiRequest(`/users/${userId}`, {
        method: 'PUT',
        body: JSON.stringify(data),
      });
    } catch (error) {
      return { success: false, error: error.message };
    }
  },

  search: async (query, role) => {
    try {
      const params = new URLSearchParams();
      if (query) params.append('q', query);
      if (role) params.append('role', role);
      return await apiRequest(`/users/search?${params.toString()}`);
    } catch (error) {
      return { success: false, error: error.message };
    }
  },
};


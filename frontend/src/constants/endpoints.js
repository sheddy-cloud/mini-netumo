export const API_URL = 'http://localhost/api'

const ENDPOINTS = {
  LOGIN: `${API_URL}/users/`,
  LOGOUT: `${API_URL}/auth/signout/`, // Assuming this is for your auth service
  TARGET: `${API_URL}/targets/`,
  REGISTER: `${API_URL}/users/`,
  STATUS_LOGS: `${API_URL}/statuslogs/`, // New endpoint
  DOMAIN_CHECKS: `${API_URL}/domainChecks/`, // New endpoint
  CERTIFICATE_CHECKS: `${API_URL}/certificateChecks/`, // New endpoint
  ALERTS: `${API_URL}/alerts/` // New endpoint for alerts
}

export default ENDPOINTS

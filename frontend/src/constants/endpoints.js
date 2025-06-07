export const API_URL = 'http://127.0.0.1:8001'

const ENDPOINTS = {
  LOGIN: `${API_URL}/auth/login/`,
  LOGOUT: `${API_URL}/auth/signout/`,
  TARGET: `${API_URL}/targets/`,
  REGISTER: `${API_URL}/auth/register/`,
  STATUS_LOGS: `${API_URL}/statuslogs/`, // New endpoint
  DOMAIN_CHECKS: `${API_URL}/domainchecks/`, // New endpoint
  CERTIFICATE_CHECKS: `${API_URL}/certificatechecks/`, // New endpoint
  ALERTS: `${API_URL}/alerts/` // New endpoint for alerts
}

export default ENDPOINTS

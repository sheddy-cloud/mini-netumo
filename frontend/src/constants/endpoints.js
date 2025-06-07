export const API_URL = 'http://127.0.0.1:8001'

const ENDPOINTS = {
  LOGIN: `${API_URL}/auth/login/`,
  LOGOUT: `${API_URL}/auth/signout/`,
  TARGET: `${API_URL}/targets/`,
  REGISTER: `${API_URL}/auth/register/`,
  STATUS_LOGS: `${API_URL}/statuslogs/`,
  DOMAIN_CHECKS: `${API_URL}/domainChecks/`,
  CERTIFICATE_CHECKS: `${API_URL}/certificateChecks/`,
  ALERTS: `${API_URL}/alerts/`,
  USER_PROFILE: `${API_URL}/auth/me/`  // <-- added this endpoint
}

export default ENDPOINTS

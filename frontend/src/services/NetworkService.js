import axios from 'axios'
import { API_URL } from '../constants/endpoints'

export default net = axios.create({
    baseURL: API_URL,
    timeout: 100000,
    headers: {},
})

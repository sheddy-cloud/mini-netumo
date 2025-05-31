import axios from 'axios'
import { API_URL } from '../constants/endpoints'

const net = axios.create({
    baseURL: API_URL,
    timeout: 100000,
    headers: {},
})

export default net

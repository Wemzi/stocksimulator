import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  withCredentials: false,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default {
  getStocks() {
    return apiClient.get('/stocks/')
  }
}
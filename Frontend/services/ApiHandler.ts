import axios from 'axios';

const axiosInstance: Axios.AxiosInstance = axios.create({
  baseURL: 'http://localhost:8080',
  headers: {
    "Content-Type": "application/json",
  },
});

export default axiosInstance;
import axios from 'axios';

const axiosInstance: Axios.AxiosInstance = axios.create({
  baseURL: 'http://localhost:8080',
});

export default axiosInstance;
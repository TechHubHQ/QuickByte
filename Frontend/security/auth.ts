import axiosInstance from '../services/ApiHandler';
import { TokenResponse, Auth } from '../types/apiTypeChecker';

const tokenEndpoint = '/validate-token';

const auth: Auth = {
  async validateToken(token: string): Promise<TokenResponse | null> {
    try {
      const response = await axiosInstance.post(`${tokenEndpoint}`, { token: `Bearer ${token}` });
      return response.data as TokenResponse;
    } catch (error) {
      console.error('Error validating token:', error);
      return null;
    }
  },

  async makeRequest<T>(endpoint: string, data: any): Promise<T | null> {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('No token found');
    }

    const validatedToken = await this.validateToken(token);
    if (!validatedToken) {
      throw new Error('Invalid token');
    }

    try {
      const response = await axiosInstance.post(`${endpoint}`, { ...data, token: `Bearer ${token}` });
      return response.data as T;
    } catch (error) {
      console.error('Error making request:', error);
      return null;
    }
  },
};

export default auth;
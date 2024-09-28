export interface TestResponse {
  message: string;
}

export interface TokenResponse {
  username: string;
}

export interface Auth {
  validateToken(token: string): Promise<TokenResponse | null>;
  makeRequest<T>(endpoint: string, data: any): Promise<T | null>;
}

export interface AuthResponse {
  token: string
}
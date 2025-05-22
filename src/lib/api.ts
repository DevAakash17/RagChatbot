import axios from 'axios';

// Define the API base URLs
const AUTH_API_URL = 'http://0.0.0.0:8005';
const RAG_API_URL = 'http://0.0.0.0:8002/api/v1';

// Define the types for our API requests and responses
export interface QueryRequest {
  query: string;
  collection_name: string;
  prev_queries?: string[];
}

export interface TokenUsage {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
}

export interface ContextDocument {
  id: string;
  text: string;
  score: number;
  metadata?: Record<string, any>;
}

export interface QueryResponse {
  text: string;
  model: string;
  usage: TokenUsage;
  finish_reason?: string;
  context_documents: ContextDocument[];
}

// Authentication interfaces
export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  id: string;
  username: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    username: string;
  };
}

// Create axios instances for different APIs
const authApi = axios.create({
  baseURL: AUTH_API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

const ragApi = axios.create({
  baseURL: RAG_API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Add auth token to requests if available
authApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Define the API functions
export const apiService = {
  /**
   * Send a query to the RAG Engine
   * @param query The user's query
   * @param collectionName The name of the collection to query
   * @returns The query response
   */
  async sendQuery(query: string, collectionName: string = 'insurance_documents', prevQueries?: string[]): Promise<QueryResponse> {
    try {
      const response = await ragApi.post<QueryResponse>('/query', {
        query,
        collection_name: collectionName,
        prev_queries: prevQueries,
      });
      return response.data;
    } catch (error) {
      console.error('Error sending query:', error);
      throw error;
    }
  },

  /**
   * Login a user
   * @param username The username
   * @param password The password
   * @returns The login response with user information
   */
  async login(username: string, password: string): Promise<LoginResponse> {
    try {
      const response = await authApi.post<LoginResponse>('/auth/login', {
        username,
        password,
      });
      // Store the user info in localStorage
      localStorage.setItem('user_id', response.data.id);
      localStorage.setItem('username', response.data.username);
      localStorage.setItem('is_authenticated', 'true');
      return response.data;
    } catch (error) {
      console.error('Error logging in:', error);
      throw error;
    }
  },

  /**
   * Register a new user
   * @param username The username
   * @param password The password
   * @returns The authentication response
   */
  async register(username: string, password: string): Promise<AuthResponse> {
    try {
      const response = await authApi.post<AuthResponse>('/auth/register', {
        username,
        password,
      });
      return response.data;
    } catch (error) {
      console.error('Error registering:', error);
      throw error;
    }
  },

  /**
   * Logout the current user
   */
  logout() {
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
    localStorage.removeItem('is_authenticated');
  },

  /**
   * Check if the user is authenticated
   * @returns True if the user is authenticated
   */
  isAuthenticated(): boolean {
    return localStorage.getItem('is_authenticated') === 'true';
  },

  /**
   * Get the current user
   * @returns The current user or null if not authenticated
   */
  getCurrentUser(): LoginResponse | null {
    const id = localStorage.getItem('user_id');
    const username = localStorage.getItem('username');

    if (id && username) {
      return { id, username };
    }

    return null;
  }
};

import axios from 'axios';

// Define the API base URL
const API_BASE_URL = 'http://0.0.0.0:8002/api/v1';

// Define the types for our API requests and responses
export interface QueryRequest {
  query: string;
  collection_name: string;
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

// Create an axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Define the API functions
export const apiService = {
  /**
   * Send a query to the RAG Engine
   * @param query The user's query
   * @param collectionName The name of the collection to query
   * @returns The query response
   */
  async sendQuery(query: string, collectionName: string = 'insurance_documents'): Promise<QueryResponse> {
    try {
      const response = await api.post<QueryResponse>('/query', {
        query,
        collection_name: collectionName,
      });
      return response.data;
    } catch (error) {
      console.error('Error sending query:', error);
      throw error;
    }
  },
};

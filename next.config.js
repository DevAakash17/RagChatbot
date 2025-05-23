/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable strict mode for React
  reactStrictMode: true,

  // Configure server-side behavior
  serverRuntimeConfig: {
    // Will only be available on the server side
    authServiceUrl: process.env.AUTH_SERVICE_URL || 'http://localhost:8005',
    // Remove the /api/v1 suffix from the RAG service URL to avoid path duplication
    ragServiceUrl: process.env.RAG_SERVICE_URL || 'http://localhost:8003',
  },

  // Configure both client and server side behavior
  publicRuntimeConfig: {
    // Will be available on both server and client
    apiBasePath: process.env.API_BASE_PATH || '',
  },
}

module.exports = nextConfig

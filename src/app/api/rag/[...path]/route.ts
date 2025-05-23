import { NextRequest, NextResponse } from 'next/server';
import getConfig from 'next/config';

// Get server-side configuration
const { serverRuntimeConfig } = getConfig();

// Internal URL for the RAG service (only accessible from the server)
// Remove the /api/v1 suffix as it's causing path duplication
const RAG_SERVICE_URL = (serverRuntimeConfig.ragServiceUrl || 'http://localhost:8003').replace(/\/api\/v1$/, '');

/**
 * Handle all RAG service API requests
 * This acts as a proxy to forward requests to the RAG service
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  const path = params.path.join('/');
  const url = new URL(request.url);
  const queryString = url.search;

  try {
    // Construct the correct path for the RAG service
    const fullPath = `/api/v1/${path}`;
    console.log(`Forwarding request to: ${RAG_SERVICE_URL}${fullPath}${queryString}`);

    const response = await fetch(`${RAG_SERVICE_URL}${fullPath}${queryString}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...(request.headers.get('Authorization')
          ? { 'Authorization': request.headers.get('Authorization') as string }
          : {})
      },
    });

    const data = await response.json();

    return NextResponse.json(data, {
      status: response.status,
    });
  } catch (error) {
    console.error(`Error proxying GET request to RAG service: ${error}`);
    return NextResponse.json(
      { error: 'Failed to connect to RAG service' },
      { status: 500 }
    );
  }
}

/**
 * Handle POST requests to RAG service
 */
export async function POST(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  const path = params.path.join('/');

  try {
    const body = await request.json();

    // Construct the correct path for the RAG service
    const fullPath = `/api/v1/${path}`;
    console.log(`Forwarding request to: ${RAG_SERVICE_URL}${fullPath}`);

    const response = await fetch(`${RAG_SERVICE_URL}${fullPath}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(request.headers.get('Authorization')
          ? { 'Authorization': request.headers.get('Authorization') as string }
          : {})
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();

    return NextResponse.json(data, {
      status: response.status,
    });
  } catch (error) {
    console.error(`Error proxying POST request to RAG service: ${error}`);
    return NextResponse.json(
      { error: 'Failed to connect to RAG service' },
      { status: 500 }
    );
  }
}

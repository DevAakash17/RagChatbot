import { NextRequest, NextResponse } from 'next/server';
import getConfig from 'next/config';

// Get server-side configuration
const { serverRuntimeConfig } = getConfig();

// Internal URL for the auth service (only accessible from the server)
const AUTH_SERVICE_URL = serverRuntimeConfig.authServiceUrl || 'http://localhost:8005';

/**
 * Handle all auth service API requests
 * This acts as a proxy to forward requests to the auth service
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  const path = params.path.join('/');
  const url = new URL(request.url);
  const queryString = url.search;

  try {
    const response = await fetch(`${AUTH_SERVICE_URL}/${path}${queryString}`, {
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
    console.error(`Error proxying GET request to auth service: ${error}`);
    return NextResponse.json(
      { error: 'Failed to connect to authentication service' },
      { status: 500 }
    );
  }
}

/**
 * Handle POST requests to auth service
 */
export async function POST(
  request: NextRequest,
  { params }: { params: { path: string[] } }
) {
  const path = params.path.join('/');

  try {
    const body = await request.json();

    const response = await fetch(`${AUTH_SERVICE_URL}/${path}`, {
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
    console.error(`Error proxying POST request to auth service: ${error}`);
    return NextResponse.json(
      { error: 'Failed to connect to authentication service' },
      { status: 500 }
    );
  }
}

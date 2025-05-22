# RAG Chatbot with Authentication

A Next.js frontend for a Retrieval-Augmented Generation (RAG) chatbot that interacts with a FastAPI backend, featuring user authentication.

## Features

- User authentication (login/register)
- Secure password storage with bcrypt encryption
- JWT-based authentication
- Chat interface with user and bot messages
- Markdown rendering for bot responses
- Auto-scrolling to the latest message
- Loading indicators
- Error handling
- Reset chat functionality
- Typing animation for bot responses

## Tech Stack

- Next.js (React + TypeScript)
- Tailwind CSS (for styling)
- ShadCN UI (for components)
- Axios (for API requests)
- React Markdown (for rendering markdown)

## Prerequisites

- Node.js 16.8 or later
- Python 3.8+
- MongoDB
- npm or yarn

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure MongoDB:
   - Make sure MongoDB is running
   - Update the `.env` file with your MongoDB connection string if needed

5. Run the backend server:
   ```bash
   python main.py
   ```
   The server will run at http://0.0.0.0:8005

### Frontend Setup

1. Navigate to the project root directory

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## API Integration

The frontend communicates with two backend services:

1. Authentication API at `http://0.0.0.0:8005` for user management
2. RAG Engine API at `http://0.0.0.0:8002/api/v1` for query processing

Make sure both backend servers are running before using the chat interface.

### API Endpoints

#### Authentication API (8005)
- `POST /auth/login`: Authenticate a user
- `POST /auth/register`: Register a new user
- `GET /auth/me`: Get current user information

#### RAG Engine API (8002)
- `POST /api/v1/query`: Send a query to the RAG engine

## Project Structure

- `src/app`: Next.js app router pages
  - `src/app/login`: Login page
- `src/components`: React components
  - `src/components/auth`: Authentication-related components
  - `src/components/chat`: Chat-related components
  - `src/components/ui`: UI components (Button, Input, etc.)
- `src/lib`: Utility functions, API service, and types
- `backend`: FastAPI backend for authentication and RAG

## License

MIT

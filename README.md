# RAG Chatbot Frontend

A Next.js frontend for a Retrieval-Augmented Generation (RAG) chatbot that interacts with a FastAPI backend.

## Features

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
- npm or yarn

## Getting Started

1. Install dependencies:

```bash
npm install
# or
yarn install
```

2. Run the development server:

```bash
npm run dev
# or
yarn dev
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## API Integration

The frontend communicates with the RAG Engine backend API at `http://0.0.0.0:8002/api/v1/query`. Make sure the backend server is running before using the chat interface.

## Project Structure

- `src/app`: Next.js app router pages
- `src/components`: React components
  - `src/components/chat`: Chat-related components
  - `src/components/ui`: UI components (Button, Input, etc.)
- `src/lib`: Utility functions, API service, and types

## License

MIT

FROM python:3.13.1-slim AS base

# Install Node.js and required dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Verify Node.js version (v22.16.0 is installed by default)
RUN node -v

# Set working directory
WORKDIR /chatbot

# Copy Python requirements
COPY requirements.txt .

ENV PIP_NO_CACHE_DIR=1
ENV TMPDIR=/tmp

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set Python path to include the current directory
ENV PYTHONPATH="${PYTHONPATH}:/chatbot"

# Copy Node.js package.json
COPY package.json .

# Install Node.js dependencies
RUN npm install

# Copy the rest of the application
COPY . /chatbot

# Build the Next.js application
RUN npm run build

# Expose ports
# Frontend
EXPOSE 3000
# Backend services
EXPOSE 8000 8001 8002

# Make the startup script executable
RUN chmod +x /chatbot/start.sh

# Set the entrypoint
ENTRYPOINT ["/chatbot/start.sh"]

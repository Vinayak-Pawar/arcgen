# Multi-stage build for Arcgen AI-powered system design tool

# Stage 1: Python backend
FROM python:3.11-slim as backend

# Set working directory
WORKDIR /app/backend

# Install system dependencies for PDF processing
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Create directories for file storage
RUN mkdir -p diagram_history

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run the backend
CMD ["python", "main.py"]

# Stage 2: Node.js frontend
FROM node:18-alpine as frontend

# Set working directory
WORKDIR /app/frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy frontend code
COPY frontend/ .

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

# Run the frontend
CMD ["npm", "start"]

# Stage 3: Final combined image (optional - for single container deployment)
FROM python:3.11-slim as combined

# Install Node.js for frontend
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy and setup backend
COPY backend/ ./backend/
WORKDIR /app/backend
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p diagram_history

# Copy and setup frontend
COPY frontend/ ./frontend/
WORKDIR /app/frontend
RUN npm ci --only=production && npm run build

# Create startup script
RUN echo '#!/bin/bash\n\
cd /app/backend && python main.py &\n\
cd /app/frontend && npm start' > /app/start.sh && \
    chmod +x /app/start.sh

# Expose ports
EXPOSE 8000 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000 && curl -f http://localhost:3000 || exit 1

# Run both services
CMD ["/app/start.sh"]
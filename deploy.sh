#!/bin/bash

# Arcgen Deployment Script
# This script helps deploy Arcgen using Docker Compose

set -e

echo "🚀 Arcgen Deployment Script"
echo "=========================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    if [ -f env-example.txt ]; then
        cp env-example.txt .env
        echo "✅ Created .env file. Please edit it with your API keys."
        echo "⚠️  IMPORTANT: Edit the .env file with your actual API keys before proceeding!"
        read -p "Press Enter after you've configured your .env file..."
    else
        echo "❌ env-example.txt not found. Please create your .env file manually."
        exit 1
    fi
fi

# Ask user which deployment mode to use
echo ""
echo "Choose deployment mode:"
echo "1) Separate containers (backend + frontend) - Recommended for development"
echo "2) Combined container (single container) - Easier for simple deployments"
echo "3) With Redis caching - Full production setup"
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "🏗️  Building and starting separate containers..."
        docker-compose up --build -d backend frontend
        ;;
    2)
        echo "🏗️  Building and starting combined container..."
        docker-compose --profile combined up --build -d combined
        ;;
    3)
        echo "🏗️  Building and starting with Redis caching..."
        docker-compose --profile with-redis up --build -d backend frontend redis
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service health..."

# Check backend
if curl -f http://localhost:8000/ &>/dev/null; then
    echo "✅ Backend is running at http://localhost:8000"
else
    echo "❌ Backend is not responding"
fi

# Check frontend
if curl -f http://localhost:3000 &>/dev/null; then
    echo "✅ Frontend is running at http://localhost:3000"
else
    echo "❌ Frontend is not responding"
fi

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "🌐 Access Arcgen at: http://localhost:3000"
echo "📚 API documentation: http://localhost:8000/docs"
echo ""
echo "📋 Useful commands:"
echo "  • View logs: docker-compose logs -f"
echo "  • Stop services: docker-compose down"
echo "  • Restart: docker-compose restart"
echo ""
echo "📁 Persistent data is stored in:"
echo "  • ./backend/diagram_history (diagram versions)"
echo "  • ./backend/uploads (uploaded files)"

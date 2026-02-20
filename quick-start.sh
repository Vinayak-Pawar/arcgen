#!/bin/bash

# =============================================================================
# Arcgen Quick Start (Simplified)
# For debugging - shows all output directly in terminal
# =============================================================================

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}Starting Arcgen...${NC}\n"

# Check .env
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Warning: .env file not found${NC}"
    echo "Creating from env-example.txt..."
    cp env-example.txt .env
    echo -e "${YELLOW}Please edit .env and add your API keys, then run this script again${NC}"
    exit 1
fi

# Setup backend
echo -e "${BLUE}[1/4] Setting up backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

echo -e "${GREEN}✓ Backend ready${NC}\n"

# Setup frontend
echo -e "${BLUE}[2/4] Setting up frontend...${NC}"
cd ../frontend

if [ ! -d "node_modules" ]; then
    npm install
fi

echo -e "${GREEN}✓ Frontend ready${NC}\n"

# Start backend
echo -e "${BLUE}[3/4] Starting backend server...${NC}"
cd ../backend
source venv/bin/activate

# Clean up old processes
lsof -ti:8000 | xargs kill -9 2>/dev/null || true

# Start backend in background
uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait and check
echo "Waiting for backend to start..."
for i in {1..10}; do
    sleep 1
    if curl -s http://localhost:8000/ >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend running on http://localhost:8000${NC}\n"
        break
    fi
    echo -n "."
done

# Start frontend
echo -e "${BLUE}[4/4] Starting frontend server...${NC}"
cd ../frontend

# Clean up old processes
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Start frontend in background
npm run dev &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

# Wait and check
echo "Waiting for frontend to start..."
for i in {1..20}; do
    sleep 1
    if curl -s http://localhost:3000/ >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Frontend running on http://localhost:3000${NC}\n"
        break
    fi
    echo -n "."
done

# Save PIDs
cd ..
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

# Success
echo ""
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}   🚀 Arcgen is Running!${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo ""
echo -e "  Frontend:  ${BLUE}http://localhost:3000${NC}"
echo -e "  Backend:   ${BLUE}http://localhost:8000${NC}"
echo -e "  API Docs:  ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}To stop: ./stop.sh${NC}"
echo ""

# Open browser
sleep 2
if command -v open &> /dev/null; then
    open http://localhost:3000
fi

echo "Servers are running in background."
echo "Check logs:"
echo "  Backend:  tail -f backend/venv/lib/python*/site-packages/uvicorn/logs/* 2>/dev/null || ps aux | grep uvicorn"
echo "  Frontend: ps aux | grep 'next dev'"
echo ""

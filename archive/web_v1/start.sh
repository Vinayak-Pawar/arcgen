#!/bin/bash

# Kill any existing processes on ports 3000 and 8000
lsof -ti:3000 | xargs kill -9 2>/dev/null
lsof -ti:8000 | xargs kill -9 2>/dev/null

echo "Starting Backend (FastAPI)..."
cd backend
uvicorn main:app --port 8000 &
cd ..
BACKEND_PID=$!

echo "Starting Frontend (Next.js)..."
cd frontend
npm run dev &
FRONTEND_PID=$!

echo "Arcgen is running!"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo "Press CTRL+C to stop both servers."

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID

#!/bin/bash

# =============================================================================
# Arcgen Startup Script
# Automatically sets up and starts both backend and frontend servers
# =============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# =============================================================================
# Helper Functions
# =============================================================================

print_header() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

check_command() {
    if command -v "$1" &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_error "$1 is not installed"
        return 1
    fi
}

# =============================================================================
# Check Prerequisites
# =============================================================================

print_header "Checking Prerequisites"

MISSING_DEPS=0

# Check Python
if check_command python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
    print_info "Python version: $PYTHON_VERSION"
else
    print_error "Python 3 is required. Install from: https://www.python.org/"
    MISSING_DEPS=1
fi

# Check Node.js
if check_command node; then
    NODE_VERSION=$(node --version)
    print_info "Node.js version: $NODE_VERSION"
else
    print_error "Node.js is required. Install from: https://nodejs.org/"
    MISSING_DEPS=1
fi

# Check npm
if check_command npm; then
    NPM_VERSION=$(npm --version)
    print_info "npm version: $NPM_VERSION"
else
    print_error "npm is required (usually comes with Node.js)"
    MISSING_DEPS=1
fi

if [ $MISSING_DEPS -eq 1 ]; then
    print_error "Please install missing dependencies and try again"
    exit 1
fi

# =============================================================================
# Check Environment Configuration
# =============================================================================

print_header "Checking Environment Configuration"

if [ ! -f ".env" ]; then
    print_warning ".env file not found"
    if [ -f "env-example.txt" ]; then
        print_info "Creating .env from env-example.txt..."
        cp env-example.txt .env
        print_warning "Please edit .env file and add your API keys"
        print_info "Opening .env file for editing..."
        
        # Try to open with default editor
        if command -v nano &> /dev/null; then
            nano .env
        elif command -v vim &> /dev/null; then
            vim .env
        elif command -v open &> /dev/null; then
            open .env
        else
            print_warning "Please manually edit .env file with your API keys"
        fi
    else
        print_error "env-example.txt not found. Cannot create .env"
        exit 1
    fi
else
    print_success ".env file exists"
    
    # Check if API key is configured
    if grep -q "your_nvidia_api_key_here" .env || grep -q "your-openai-key-here" .env; then
        print_warning "API keys might not be configured yet"
        print_info "Make sure to set your API keys in .env file"
    else
        print_success "API keys appear to be configured"
    fi
fi

# =============================================================================
# Setup Backend
# =============================================================================

print_header "Setting Up Backend"

cd "$SCRIPT_DIR/backend"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Install/Update dependencies
print_info "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
print_success "Python dependencies installed"

# =============================================================================
# Setup Frontend
# =============================================================================

print_header "Setting Up Frontend"

cd "$SCRIPT_DIR/frontend"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    print_info "Installing Node.js dependencies (this may take a few minutes)..."
    npm install --silent
    print_success "Node.js dependencies installed"
else
    print_success "Node.js dependencies already installed"
fi

# =============================================================================
# Start Servers
# =============================================================================

print_header "Starting Servers"

# Kill any existing processes on ports 8000 and 3000
print_info "Checking for existing processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
print_success "Ports cleared"

# Start backend server in background
print_info "Starting backend server on http://localhost:8000..."
cd "$SCRIPT_DIR/backend"
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 > "$SCRIPT_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > "$SCRIPT_DIR/.backend.pid"

# Wait for backend to start with retry logic
print_info "Waiting for backend to initialize..."
MAX_RETRIES=15
RETRY_COUNT=0
BACKEND_READY=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    sleep 1
    if curl -s http://localhost:8000/ > /dev/null 2>&1; then
        BACKEND_READY=true
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo -n "."
done

echo ""

if [ "$BACKEND_READY" = true ]; then
    print_success "Backend server started (PID: $BACKEND_PID)"
else
    print_error "Backend server failed to start after $MAX_RETRIES seconds"
    print_info "Last 20 lines of backend.log:"
    tail -20 "$SCRIPT_DIR/backend.log"
    exit 1
fi

# Start frontend server in background
print_info "Starting frontend server on http://localhost:3000..."
cd "$SCRIPT_DIR/frontend"
npm run dev > "$SCRIPT_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > "$SCRIPT_DIR/.frontend.pid"

# Wait for frontend to start with retry logic
print_info "Waiting for frontend to initialize..."
MAX_RETRIES=30
RETRY_COUNT=0
FRONTEND_READY=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    sleep 1
    if curl -s http://localhost:3000/ > /dev/null 2>&1; then
        FRONTEND_READY=true
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo -n "."
done

echo ""

if [ "$FRONTEND_READY" = true ]; then
    print_success "Frontend server started (PID: $FRONTEND_PID)"
else
    print_error "Frontend server failed to start after $MAX_RETRIES seconds"
    print_info "Last 20 lines of frontend.log:"
    tail -20 "$SCRIPT_DIR/frontend.log"
    exit 1
fi

# =============================================================================
# Success Message
# =============================================================================

print_header "🚀 Arcgen is Ready!"

echo ""
echo -e "${GREEN}✓ Backend:  http://localhost:8000${NC}"
echo -e "${GREEN}✓ Frontend: http://localhost:3000${NC}"
echo -e "${GREEN}✓ API Docs: http://localhost:8000/docs${NC}"
echo ""
echo -e "${YELLOW}Logs:${NC}"
echo -e "  Backend:  tail -f $SCRIPT_DIR/backend.log"
echo -e "  Frontend: tail -f $SCRIPT_DIR/frontend.log"
echo ""
echo -e "${YELLOW}To stop servers:${NC}"
echo -e "  Run: ./stop.sh"
echo -e "  Or:  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo -e "${BLUE}Opening browser...${NC}"

# Wait a bit more for full startup
sleep 2

# Open browser
if command -v open &> /dev/null; then
    open http://localhost:3000
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000
elif command -v sensible-browser &> /dev/null; then
    sensible-browser http://localhost:3000
else
    print_warning "Please manually open http://localhost:3000 in your browser"
fi

echo ""
print_success "Arcgen is running! Press Ctrl+C to view logs, or run ./stop.sh to stop servers"
echo ""

# Keep script running and tail logs
trap "echo ''; print_info 'To stop servers, run: ./stop.sh'; exit 0" INT

tail -f "$SCRIPT_DIR/backend.log" "$SCRIPT_DIR/frontend.log"

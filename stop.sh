#!/bin/bash

# =============================================================================
# Arcgen Stop Script
# Stops both backend and frontend servers
# =============================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

echo ""
print_info "Stopping Arcgen servers..."
echo ""

# Stop processes by PID files
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        print_success "Backend server stopped (PID: $BACKEND_PID)"
    else
        print_info "Backend server was not running"
    fi
    rm .backend.pid
fi

if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        print_success "Frontend server stopped (PID: $FRONTEND_PID)"
    else
        print_info "Frontend server was not running"
    fi
    rm .frontend.pid
fi

# Force kill any remaining processes on ports 8000 and 3000
print_info "Cleaning up any remaining processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

print_success "All servers stopped"
echo ""
print_info "To start again, run: ./start.sh"
echo ""

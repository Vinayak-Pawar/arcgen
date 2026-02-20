#!/bin/bash

# Cleanup script for Arcgen test files
# Use this to remove temporary test files while keeping the application

echo ""
echo "🧹 Arcgen Cleanup Script"
echo "================================"
echo ""
echo "This script will clean up test files and temporary data."
echo "Your application code will NOT be affected."
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo ""
echo "Cleaning up..."
echo ""

# Remove test scripts (optional - ask first)
read -p "Remove test scripts? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f test_*.py
    echo "✓ Removed test scripts"
fi

# Remove log files
read -p "Remove log files? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f backend.log frontend.log
    echo "✓ Removed log files"
fi

# Remove PID files
rm -f .backend.pid .frontend.pid
echo "✓ Removed PID files"

# Clean Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "✓ Cleaned Python cache"

# Clean Node.js cache (optional)
read -p "Clean Node.js cache? This will require npm install next time (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf frontend/.next
    echo "✓ Cleaned Next.js build cache"
fi

echo ""
echo "================================"
echo "✅ Cleanup complete!"
echo ""
echo "Your application is still ready to run:"
echo "  ./start.sh  - Start servers"
echo ""

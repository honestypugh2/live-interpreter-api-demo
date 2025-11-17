#!/bin/bash

# Azure Live Interpreter React App - Quick Start Script
# This script starts both the backend and frontend servers

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/../.."
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Azure Live Interpreter - Quick Start${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if .env file exists
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo -e "${RED}❌ Error: .env file not found in project root${NC}"
    echo -e "${YELLOW}Please create a .env file with your Azure Speech Service credentials${NC}"
    echo ""
    echo "Example .env file:"
    echo "SPEECH_KEY=your_key_here"
    echo "SPEECH_REGION=eastus"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ .env file found${NC}"

# Check Python
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python is not installed${NC}"
    exit 1
fi

PYTHON_CMD=$(command -v python3 || command -v python)
echo -e "${GREEN}✓ Python found: $PYTHON_CMD${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"

# Check npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ npm found: $(npm --version)${NC}"

echo ""

# Check if backend dependencies are installed
echo -e "${BLUE}Checking backend dependencies...${NC}"
if ! $PYTHON_CMD -c "import fastapi" &> /dev/null; then
    echo -e "${YELLOW}⚠ Backend dependencies not found. Installing...${NC}"
    cd "$PROJECT_ROOT"
    pip install -r requirements.txt
    echo -e "${GREEN}✓ Backend dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Backend dependencies found${NC}"
fi

# Check if frontend dependencies are installed
echo -e "${BLUE}Checking frontend dependencies...${NC}"
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo -e "${YELLOW}⚠ Frontend dependencies not found. Installing...${NC}"
    cd "$FRONTEND_DIR"
    npm install
    echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
else
    echo -e "${GREEN}✓ Frontend dependencies found${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Starting servers...${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down servers...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    echo -e "${GREEN}✓ Servers stopped${NC}"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start backend
echo -e "${BLUE}Starting backend server...${NC}"
cd "$BACKEND_DIR"
$PYTHON_CMD main.py > backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
echo -e "${YELLOW}Waiting for backend to be ready...${NC}"
sleep 3

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo -e "${RED}❌ Backend failed to start. Check backend.log for errors${NC}"
    cat backend.log
    exit 1
fi

# Check backend health
MAX_RETRIES=10
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend is ready (http://localhost:8000)${NC}"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
        echo -e "${RED}❌ Backend health check failed${NC}"
        echo "Backend log:"
        tail -20 backend.log
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
    sleep 1
done

# Start frontend
echo -e "${BLUE}Starting frontend server...${NC}"
cd "$FRONTEND_DIR"
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for frontend to start
echo -e "${YELLOW}Waiting for frontend to be ready...${NC}"
sleep 3

# Check if frontend is running
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo -e "${RED}❌ Frontend failed to start. Check frontend.log for errors${NC}"
    cat frontend.log
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Extract the actual port from the log file
FRONTEND_PORT=""
MAX_RETRIES=10
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if [ -f frontend.log ]; then
        # Extract port from Vite output (looks for "Local:   http://localhost:XXXX/")
        FRONTEND_PORT=$(grep -oP "Local:\s+http://localhost:\K\d+" frontend.log | tail -1)
        if [ ! -z "$FRONTEND_PORT" ]; then
            if curl -s "http://localhost:$FRONTEND_PORT" > /dev/null 2>&1; then
                echo -e "${GREEN}✓ Frontend is ready (http://localhost:$FRONTEND_PORT)${NC}"
                break
            fi
        fi
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
        echo -e "${YELLOW}⚠ Frontend might still be starting...${NC}"
        # Try to extract port anyway
        FRONTEND_PORT=$(grep -oP "Local:\s+http://localhost:\K\d+" frontend.log | tail -1)
        if [ -z "$FRONTEND_PORT" ]; then
            FRONTEND_PORT="5173"
        fi
        break
    fi
    sleep 1
done

# Default to 5173 if we couldn't detect the port
if [ -z "$FRONTEND_PORT" ]; then
    FRONTEND_PORT="5173"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ All servers are running!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Access the application:${NC}"
echo -e "  Frontend: ${GREEN}http://localhost:$FRONTEND_PORT${NC}"
echo -e "  Backend:  ${GREEN}http://localhost:8000${NC}"
echo -e "  API Docs: ${GREEN}http://localhost:8000/docs${NC}"
echo ""
echo -e "${BLUE}Logs:${NC}"
echo -e "  Backend:  ${YELLOW}$BACKEND_DIR/backend.log${NC}"
echo -e "  Frontend: ${YELLOW}$FRONTEND_DIR/frontend.log${NC}"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"
echo ""

# Keep script running and show logs
tail -f "$BACKEND_DIR/backend.log" "$FRONTEND_DIR/frontend.log" &
TAIL_PID=$!

# Wait for user interrupt
wait $BACKEND_PID $FRONTEND_PID

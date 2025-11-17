#!/bin/bash

# Start script for React Demo App (Simulated Mode - No Backend Required)

set -e

echo "=================================================="
echo "Azure Live Interpreter - Demo Mode (Simulated)"
echo "=================================================="
echo ""

# Check if we're in the react_app directory
if [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: Please run this script from the src/react_app directory"
    echo "   cd src/react_app"
    echo "   ./start-demo.sh"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "   Please install Node.js 18 or higher: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "⚠️  Warning: Node.js version $NODE_VERSION detected. Version 18+ recommended."
fi

echo "✅ Node.js $(node --version) detected"
echo ""

# Install frontend dependencies if needed
cd frontend
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
    echo ""
fi

echo "=================================================="
echo "Starting Demo Mode (No Backend Required)"
echo "=================================================="
echo ""
echo "🎬 Demo Features:"
echo "   • Simulated council meeting with pre-scripted dialogue"
echo "   • English ⇄ Spanish translation demo"
echo "   • No microphone or Azure API required"
echo "   • Perfect for demonstrations and training"
echo ""
echo "📝 Note: If port 5173 is in use, Vite will automatically"
echo "         choose the next available port (5174, 5175, etc.)"
echo ""
echo "Press Ctrl+C to stop"
echo "=================================================="
echo ""

# Start frontend in demo mode
echo "🚀 Starting Vite development server..."
echo ""
echo "📝 To access the demo, open your browser to:"
echo "   http://localhost:5173/index-demo.html"
echo "   (or the next available port if 5173 is in use)"
echo ""
npm run dev:demo

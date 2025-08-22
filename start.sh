#!/bin/bash

# Stock Advisor Startup Script
# This script starts both the backend and frontend services

echo "🚀 Starting Stock Advisor Application..."
echo "========================================"

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0  # Port is in use (service is running)
    else
        return 1  # Port is not in use
    fi
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ and try again."
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is not installed. Please install npm and try again."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Check if ports are already in use by other services
echo "🔍 Checking if ports are available..."

if check_port 8000; then
    echo "❌ Port 8000 is already in use by another service. Please free up the port and try again."
    exit 1
fi

if check_port 3000; then
    echo "❌ Port 3000 is already in use by another service. Please free up the port and try again."
    exit 1
fi

echo "✅ Ports are available!"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
echo "📦 Installing backend dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating example .env file..."
    cat > .env << EOF
# API Keys (Get these from the respective services)
ALPHA_VANTAGE_API_KEY=your_api_key_here
FINNHUB_API_KEY=your_api_key_here

# Application Settings
DEBUG=True
SECRET_KEY=your_secret_key_here

# Database
DATABASE_URL=sqlite:///./stock_advisor.db
EOF
    echo "📝 Please edit .env file with your actual API keys before starting the application."
    echo "🔑 Get Alpha Vantage API key from: https://www.alphavantage.co/support/#api-key"
    echo "🔑 Get Finnhub API key from: https://finnhub.io/register"
    echo ""
    read -p "Press Enter after updating .env file to continue..."
fi

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing npm packages..."
    npm install
else
    echo "Node modules already installed, skipping npm install..."
fi
cd ..

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "✅ Backend stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "✅ Frontend stopped"
    fi
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Start backend (files are in root directory)
echo "🚀 Starting backend server..."
python main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend is running
if ! check_port 8000; then
    echo "❌ Backend failed to start. Check the logs above for errors."
    cleanup
fi

echo "✅ Backend is running on http://localhost:8000"

# Start frontend
echo "🚀 Starting frontend server..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

# Wait a moment for frontend to start
sleep 8

# Check if frontend is running
if ! check_port 3000; then
    echo "❌ Frontend failed to start. Check the logs above for errors."
    cleanup
fi

echo "✅ Frontend is running on http://localhost:3000"
echo ""
echo "🎉 Stock Advisor is now running!"
echo "================================="
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for user to stop the services
wait

@echo off
REM Stock Advisor Startup Script for Windows
REM This script starts both the backend and frontend services

echo 🚀 Starting Stock Advisor Application...
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ and try again.
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm is not installed. Please install npm and try again.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed!

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found. Creating example .env file...
    (
        echo # API Keys (Get these from the respective services
        echo ALPHA_VANTAGE_API_KEY=your_api_key_here
        echo FINNHUB_API_KEY=your_api_key_here
        echo.
        echo # Application Settings
        echo DEBUG=True
        echo SECRET_KEY=your_secret_key_here
        echo.
        echo # Database
        echo DATABASE_URL=sqlite:///./stock_advisor.db
    ) > .env
    
    echo 📝 Please edit .env file with your actual API keys before starting the application.
    echo 🔑 Get Alpha Vantage API key from: https://www.alphavantage.co/support/#api-key
    echo 🔑 Get Finnhub API key from: https://finnhub.io/register
    echo.
    pause
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 🐍 Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🐍 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install backend dependencies
echo 📦 Installing backend dependencies...
pip install -r requirements.txt

REM Install frontend dependencies
echo 📦 Installing frontend dependencies...
cd frontend
npm install
cd ..

echo 🚀 Starting backend server...
start "Stock Advisor Backend" cmd /k "cd backend && call ..\venv\Scripts\activate.bat && python main.py"

REM Wait for backend to start
timeout /t 5 /nobreak >nul

echo 🚀 Starting frontend server...
start "Stock Advisor Frontend" cmd /k "cd frontend && npm start"

REM Wait for frontend to start
timeout /t 5 /nobreak >nul

echo.
echo 🎉 Stock Advisor is now running!
echo =================================
echo 🌐 Frontend: http://localhost:3000
echo 🔌 Backend API: http://localhost:8000
echo 📚 API Documentation: http://localhost:8000/docs
echo.
echo The application windows are now open in separate command prompts.
echo Close those windows to stop the services.
echo.
pause

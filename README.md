# 🚀 Stock Advisor - High-Accuracy Stock Analysis Tool

A comprehensive stock analysis platform that provides buy/sell recommendations based on advanced technical patterns and fundamental analysis. Built with FastAPI backend and React frontend.

## 🌟 Features

### **Technical Analysis**
- **50+ Technical Indicators**: RSI, MACD, Bollinger Bands, Moving Averages, Stochastic, Williams %R
- **Pattern Recognition**: Candlestick patterns, chart patterns (head & shoulders, triangles, double tops/bottoms)
- **Support/Resistance**: Dynamic level detection using clustering algorithms
- **Trend Analysis**: Multiple timeframe analysis with trend strength indicators
- **Volume Analysis**: OBV, VWAP, Money Flow Index, volume-weighted indicators

### **Fundamental Analysis**
- **Financial Ratios**: P/E, P/B, ROE, ROA, Debt-to-Equity, Current Ratio
- **Valuation Models**: DCF, DDM, Comparable company analysis
- **Scoring System**: Comprehensive scoring across 4 categories (Valuation, Profitability, Growth, Financial Health)
- **Industry Comparison**: Peer analysis and sector performance
- **Financial Statements**: Balance sheet, income statement, cash flow analysis

### **AI/ML Features**
- **Pattern Learning**: Machine learning for advanced pattern recognition
- **Risk Assessment**: Portfolio risk scoring and optimization
- **Prediction Models**: Price target predictions with confidence intervals
- **Sentiment Analysis**: News and market sentiment integration

### **User Experience**
- **Real-time Data**: Live stock quotes and market data via multiple APIs
- **Interactive Charts**: Advanced charting with multiple indicators
- **Portfolio Management**: Track positions, performance, and alerts
- **Custom Alerts**: Price, volume, and pattern-based notifications
- **Report Generation**: Detailed analysis reports and recommendations

## 🏗️ Architecture

```
Stock Advisor/
├── backend/                 # FastAPI Backend
│   ├── main.py             # Main FastAPI application
│   ├── models.py           # Database models
│   ├── database.py         # Database connection
│   ├── data_fetcher.py     # Stock data fetching
│   ├── technical_analysis.py # Technical analysis engine
│   ├── fundamental_analysis.py # Fundamental analysis engine
│   ├── config.py           # Configuration settings
│   └── requirements.txt    # Python dependencies
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── App.js          # Main app component
│   ├── package.json        # Node dependencies
│   └── tailwind.config.js  # Tailwind CSS config
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- SQLite (or PostgreSQL for production)

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**
   ```bash
   # Create .env file
   echo "ALPHA_VANTAGE_API_KEY=your_api_key_here" > .env
   echo "DEBUG=True" >> .env
   echo "SECRET_KEY=your_secret_key_here" >> .env
   ```

5. **Run the backend**
   ```bash
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`
   - Interactive API: `http://localhost:8000/redoc`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```
   
   The frontend will be available at `http://localhost:3000`

## 📊 API Endpoints

### Stock Analysis
- `GET /api/stocks/{symbol}` - Comprehensive stock analysis
- `GET /api/stocks/{symbol}/technical` - Technical analysis only
- `GET /api/stocks/{symbol}/fundamental` - Fundamental analysis only
- `GET /api/stocks/{symbol}/signals` - Buy/sell signals

### Market Data
- `GET /api/market/overview` - Market overview and sector performance

### Portfolio Management
- `GET /api/portfolios` - List portfolios
- `POST /api/portfolios` - Create portfolio
- `GET /api/portfolios/{id}` - Portfolio details

## 🔧 Configuration

### Backend Configuration (`config.py`)
```python
# API Keys
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '')
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY', '')

# Database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./stock_advisor.db')

# Technical Analysis Settings
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
BOLLINGER_PERIOD = 20

# Fundamental Analysis Settings
MIN_MARKET_CAP = 1000000000  # $1B
MAX_PE_RATIO = 100
CONFIDENCE_THRESHOLD = 0.7
```

### Frontend Configuration
The frontend automatically proxies API calls to `http://localhost:8000` during development.

## 📈 Technical Indicators

### Momentum Indicators
- **RSI (Relative Strength Index)**: Overbought/oversold conditions
- **MACD**: Trend following and momentum
- **Stochastic Oscillator**: Price momentum
- **Williams %R**: Market momentum

### Trend Indicators
- **Moving Averages**: SMA, EMA, WMA (5, 10, 20, 50, 100, 200 periods)
- **Bollinger Bands**: Volatility and price channels
- **ADX**: Trend strength
- **Parabolic SAR**: Trend reversal

### Volume Indicators
- **OBV (On-Balance Volume)**: Volume-price relationship
- **VWAP**: Volume-weighted average price
- **Money Flow Index**: Volume and price momentum
- **Volume Rate of Change**: Volume momentum

## 🎯 Pattern Recognition

### Candlestick Patterns
- Doji, Hammer, Shooting Star
- Engulfing, Harami, Morning/Evening Star
- Three White Soldiers, Three Black Crows
- And 40+ more patterns

### Chart Patterns
- Head and Shoulders
- Triangles (Ascending, Descending, Symmetrical)
- Double Tops and Bottoms
- Support and Resistance Levels

## 📊 Fundamental Analysis

### Valuation Metrics
- **P/E Ratio**: Price to earnings
- **P/B Ratio**: Price to book value
- **P/S Ratio**: Price to sales
- **PEG Ratio**: Price/earnings to growth
- **Enterprise Value**: EV/EBITDA, EV/Revenue

### Profitability Metrics
- **ROE**: Return on equity
- **ROA**: Return on assets
- **Gross Margin**: Gross profit margin
- **Operating Margin**: Operating profit margin
- **Net Margin**: Net profit margin

### Financial Health
- **Debt-to-Equity**: Leverage ratio
- **Current Ratio**: Liquidity ratio
- **Quick Ratio**: Acid test ratio
- **Interest Coverage**: Debt service ability

## 🚀 Deployment

### Backend Deployment
1. **Production Server Setup**
   ```bash
   # Install production dependencies
   pip install gunicorn uvicorn[standard]
   
   # Run with Gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

2. **Docker Deployment**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

### Frontend Deployment
1. **Build for Production**
   ```bash
   npm run build
   ```

2. **Serve Static Files**
   ```bash
   # Using nginx or serve
   npx serve -s build -l 3000
   ```

## 🔒 Security Considerations

- API keys stored in environment variables
- CORS configured for production
- Input validation and sanitization
- Rate limiting for API endpoints
- SQL injection protection via SQLAlchemy

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the code examples in the repository

## 🔮 Future Enhancements

- **Real-time WebSocket updates**
- **Advanced ML models for prediction**
- **Options analysis and strategies**
- **Cryptocurrency support**
- **Mobile applications**
- **Social trading features**
- **Advanced portfolio optimization**
- **Risk management tools**

---

**Built with ❤️ using FastAPI, React, and advanced financial analysis algorithms**

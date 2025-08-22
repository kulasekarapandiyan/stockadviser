# 🐍 Stock Advisor Backend

FastAPI-based backend for the Stock Advisor application, providing comprehensive stock analysis APIs with technical and fundamental analysis capabilities.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- SQLite (default) or PostgreSQL

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd stock-advisor/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env file with your API keys
   ALPHA_VANTAGE_API_KEY=your_api_key_here
   FINNHUB_API_KEY=your_api_key_here
   DEBUG=True
   SECRET_KEY=your_secret_key_here
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## 📊 API Documentation

- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## 🏗️ Project Structure

```
backend/
├── main.py                    # FastAPI application entry point
├── config.py                  # Configuration settings
├── database.py                # Database connection and session management
├── models.py                  # SQLAlchemy database models
├── data_fetcher.py            # Stock data fetching from multiple sources
├── technical_analysis.py      # Technical analysis engine
├── fundamental_analysis.py    # Fundamental analysis engine
├── requirements.txt           # Python dependencies
└── .env                      # Environment variables (create this)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# API Keys
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
FINNHUB_API_KEY=your_finnhub_api_key

# Database
DATABASE_URL=sqlite:///./stock_advisor.db

# Application Settings
DEBUG=True
SECRET_KEY=your_secret_key_here

# Data Settings
DEFAULT_TIMEFRAME=1d
DEFAULT_PERIOD=1y
MAX_STOCKS_PER_PORTFOLIO=100

# Technical Analysis Settings
RSI_PERIOD=14
MACD_FAST=12
MACD_SLOW=26
MACD_SIGNAL=9
BOLLINGER_PERIOD=20
BOLLINGER_STD=2

# Fundamental Analysis Settings
MIN_MARKET_CAP=1000000000
MAX_PE_RATIO=100
MIN_VOLUME=1000000

# ML Model Settings
PREDICTION_DAYS=30
CONFIDENCE_THRESHOLD=0.7
MODEL_UPDATE_FREQUENCY=1d
```

### API Keys Required

1. **Alpha Vantage API Key**
   - Sign up at: https://www.alphavantage.co/support/#api-key
   - Free tier: 5 API calls per minute, 500 per day

2. **Finnhub API Key** (Optional)
   - Sign up at: https://finnhub.io/register
   - Free tier: 60 API calls per minute

## 📊 API Endpoints

### Stock Analysis

#### Get Comprehensive Stock Analysis
```http
GET /api/stocks/{symbol}
```

**Parameters:**
- `symbol` (path): Stock symbol (e.g., AAPL, MSFT)
- `period` (query): Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
- `interval` (query): Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)

**Response:**
```json
{
  "symbol": "AAPL",
  "period": "1y",
  "interval": "1d",
  "current_price": 150.25,
  "price_change": 2.50,
  "price_change_percent": 1.69,
  "technical_analysis": {
    "indicators": {...},
    "patterns": [...],
    "signals": {...}
  },
  "fundamental_analysis": {
    "data": {...},
    "scores": {...},
    "signals": {...}
  },
  "overall_recommendation": {...}
}
```

#### Get Technical Analysis
```http
GET /api/stocks/{symbol}/technical
```

#### Get Fundamental Analysis
```http
GET /api/stocks/{symbol}/fundamental
```

#### Get Buy/Sell Signals
```http
GET /api/stocks/{symbol}/signals
```

### Market Data

#### Get Market Overview
```http
GET /api/market/overview
```

**Response:**
```json
{
  "market_indices": {
    "S&P 500": {
      "current_value": 4200.50,
      "change": 15.25,
      "change_percent": 0.36
    }
  },
  "sector_performance": {
    "Technology": {
      "etf": "XLK",
      "ytd_return": 25.5,
      "current_price": 150.25
    }
  }
}
```

### Portfolio Management

#### List Portfolios
```http
GET /api/portfolios
```

#### Create Portfolio
```http
POST /api/portfolios
```

**Request Body:**
```json
{
  "name": "My Portfolio",
  "description": "Long-term growth portfolio"
}
```

#### Get Portfolio Details
```http
GET /api/portfolios/{portfolio_id}
```

## 🔍 Technical Analysis Features

### Indicators Calculated

- **Moving Averages**: SMA (5, 10, 20, 50, 100, 200), EMA (12, 26, 50, 200), WMA (20)
- **Momentum**: RSI, MACD, Stochastic, Williams %R, ROC, Momentum, CCI
- **Trend**: ADX, Parabolic SAR, Directional Movement
- **Volatility**: Bollinger Bands, ATR
- **Volume**: OBV, VROC, VWAP, MFI

### Pattern Recognition

- **Candlestick Patterns**: 40+ patterns including Doji, Hammer, Engulfing, etc.
- **Chart Patterns**: Head & Shoulders, Triangles, Double Tops/Bottoms
- **Support/Resistance**: Dynamic level detection using DBSCAN clustering

### Signal Generation

- **RSI Signals**: Overbought (>70) / Oversold (<30)
- **MACD Signals**: Bullish/Bearish crossovers
- **Bollinger Bands**: Price at upper/lower bands
- **Moving Averages**: Golden Cross / Death Cross
- **Volume Signals**: Volume spikes and trends

## 📊 Fundamental Analysis Features

### Scoring System

- **Valuation Score** (25%): P/E, P/B, P/S, PEG ratios
- **Profitability Score** (25%): ROE, ROA, margins
- **Growth Score** (25%): Revenue and earnings growth
- **Financial Health Score** (25%): Debt ratios, liquidity

### Metrics Analyzed

- **Valuation**: P/E, P/B, P/S, PEG, EV/EBITDA
- **Profitability**: ROE, ROA, Gross/Operating/Net margins
- **Growth**: Revenue growth, earnings growth
- **Financial Health**: Debt-to-equity, current ratio, quick ratio
- **Market Data**: Market cap, beta, dividend yield

### Valuation Models

- **DCF (Discounted Cash Flow)**: Future earnings valuation
- **DDM (Dividend Discount Model)**: Dividend-based valuation
- **Peer Comparison**: Industry and sector analysis

## 🗄️ Database Models

### Core Models

- **Stock**: Basic stock information and metadata
- **Portfolio**: User portfolio definitions
- **PortfolioPosition**: Individual stock positions
- **TechnicalSignal**: Technical analysis signals
- **FundamentalScore**: Fundamental analysis scores
- **PricePrediction**: ML-based price predictions
- **MarketData**: Historical market data with indicators
- **Alert**: User-defined alerts and notifications

### Database Schema

```sql
-- Example: Stock table
CREATE TABLE stocks (
    id INTEGER PRIMARY KEY,
    symbol VARCHAR UNIQUE NOT NULL,
    company_name VARCHAR,
    sector VARCHAR,
    industry VARCHAR,
    market_cap FLOAT,
    pe_ratio FLOAT,
    pb_ratio FLOAT,
    dividend_yield FLOAT,
    beta FLOAT,
    last_updated DATETIME
);
```

## 🚀 Development

### Running in Development Mode

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or use the main.py script
python main.py
```

### Code Structure

- **Main Application** (`main.py`): FastAPI app with endpoints and routing
- **Data Layer** (`data_fetcher.py`): External API integration and data fetching
- **Analysis Engines**: Separate modules for technical and fundamental analysis
- **Database Layer** (`models.py`, `database.py`): Data persistence and models

### Adding New Features

1. **New Technical Indicators**
   - Add calculation method in `technical_analysis.py`
   - Update `calculate_all_indicators()` method
   - Add to signal generation if applicable

2. **New Fundamental Metrics**
   - Add calculation method in `fundamental_analysis.py`
   - Update scoring algorithms
   - Add to database models if needed

3. **New API Endpoints**
   - Add route in `main.py`
   - Implement business logic
   - Add error handling and validation

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

### Test Structure

```
tests/
├── test_api.py           # API endpoint tests
├── test_technical.py     # Technical analysis tests
├── test_fundamental.py   # Fundamental analysis tests
└── test_data_fetcher.py  # Data fetching tests
```

## 🚀 Production Deployment

### Using Gunicorn

```bash
# Install production dependencies
pip install gunicorn uvicorn[standard]

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build and run
docker build -t stock-advisor-backend .
docker run -p 8000:8000 stock-advisor-backend
```

### Environment Variables for Production

```bash
DEBUG=False
SECRET_KEY=your_secure_secret_key
DATABASE_URL=postgresql://user:password@localhost/stock_advisor
ALPHA_VANTAGE_API_KEY=your_production_api_key
```

## 📊 Performance Optimization

### Caching Strategies

- **Redis Cache**: Cache frequently accessed data
- **Database Indexing**: Optimize database queries
- **API Rate Limiting**: Respect external API limits

### Scaling Considerations

- **Horizontal Scaling**: Multiple worker processes
- **Load Balancing**: Nginx or similar
- **Database Optimization**: Connection pooling, query optimization

## 🔒 Security

### Security Features

- **Input Validation**: Pydantic models for request validation
- **SQL Injection Protection**: SQLAlchemy ORM
- **CORS Configuration**: Configurable cross-origin requests
- **Rate Limiting**: API usage limits
- **Environment Variables**: Secure configuration management

### Security Best Practices

- Store API keys in environment variables
- Use HTTPS in production
- Implement proper authentication and authorization
- Regular security updates
- Input sanitization and validation

## 📝 Logging

### Logging Configuration

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General information about program execution
- **WARNING**: Warning messages for potentially problematic situations
- **ERROR**: Error messages for serious problems
- **CRITICAL**: Critical errors that may prevent the program from running

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure virtual environment is activated
   - Check all dependencies are installed

2. **API Key Errors**
   - Verify API keys in `.env` file
   - Check API key validity and limits

3. **Database Errors**
   - Ensure database file is writable
   - Check database connection string

4. **Port Already in Use**
   - Change port in configuration
   - Kill existing process using the port

### Getting Help

- Check the API documentation at `/docs`
- Review error logs in console
- Create an issue in the repository
- Check external API service status

---

**Happy coding! 🚀**

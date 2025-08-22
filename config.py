import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY', '')
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY', '')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./stock_advisor.db')
    
    # Application settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    # Data settings
    DEFAULT_TIMEFRAME = '1d'
    DEFAULT_PERIOD = '1y'
    MAX_STOCKS_PER_PORTFOLIO = 100
    
    # Technical analysis settings
    RSI_PERIOD = 14
    MACD_FAST = 12
    MACD_SLOW = 26
    MACD_SIGNAL = 9
    BOLLINGER_PERIOD = 20
    BOLLINGER_STD = 2
    
    # Fundamental analysis settings
    MIN_MARKET_CAP = 1000000000  # $1B
    MAX_PE_RATIO = 100
    MIN_VOLUME = 1000000  # 1M shares
    
    # ML model settings
    PREDICTION_DAYS = 30
    CONFIDENCE_THRESHOLD = 0.7
    MODEL_UPDATE_FREQUENCY = '1d'  # Update models daily


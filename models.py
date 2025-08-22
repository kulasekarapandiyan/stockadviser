from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    company_name = Column(String)
    sector = Column(String)
    industry = Column(String)
    market_cap = Column(Float)
    pe_ratio = Column(Float)
    pb_ratio = Column(Float)
    dividend_yield = Column(Float)
    beta = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    technical_signals = relationship("TechnicalSignal", back_populates="stock")
    fundamental_scores = relationship("FundamentalScore", back_populates="stock")
    price_predictions = relationship("PricePrediction", back_populates="stock")
    portfolio_positions = relationship("PortfolioPosition", back_populates="stock")

class Portfolio(Base):
    __tablename__ = "portfolios"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    positions = relationship("PortfolioPosition", back_populates="portfolio")

class PortfolioPosition(Base):
    __tablename__ = "portfolio_positions"
    
    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    shares = Column(Float)
    avg_price = Column(Float)
    entry_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="positions")
    stock = relationship("Stock", back_populates="portfolio_positions")

class TechnicalSignal(Base):
    __tablename__ = "technical_signals"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    signal_type = Column(String)  # 'buy', 'sell', 'hold'
    confidence = Column(Float)
    indicators = Column(JSON)  # Store indicator values
    pattern_detected = Column(String)
    signal_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    stock = relationship("Stock", back_populates="technical_signals")

class FundamentalScore(Base):
    __tablename__ = "fundamental_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    overall_score = Column(Float)
    valuation_score = Column(Float)
    profitability_score = Column(Float)
    growth_score = Column(Float)
    financial_health_score = Column(Float)
    metrics = Column(JSON)  # Store all calculated metrics
    analysis_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    stock = relationship("Stock", back_populates="fundamental_scores")

class PricePrediction(Base):
    __tablename__ = "price_predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    predicted_price = Column(Float)
    confidence_interval = Column(JSON)  # Store min, max, confidence
    prediction_date = Column(DateTime)
    model_version = Column(String)
    features_used = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    stock = relationship("Stock", back_populates="price_predictions")

class MarketData(Base):
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    date = Column(DateTime)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Integer)
    adjusted_close = Column(Float)
    
    # Technical indicators
    rsi = Column(Float)
    macd = Column(Float)
    macd_signal = Column(Float)
    macd_histogram = Column(Float)
    bollinger_upper = Column(Float)
    bollinger_lower = Column(Float)
    bollinger_middle = Column(Float)
    sma_20 = Column(Float)
    sma_50 = Column(Float)
    sma_200 = Column(Float)
    
    # Fundamental data
    pe_ratio = Column(Float)
    pb_ratio = Column(Float)
    market_cap = Column(Float)
    dividend_yield = Column(Float)
    
    # Relationships
    stock = relationship("Stock")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    alert_type = Column(String)  # 'price', 'volume', 'technical', 'fundamental'
    condition = Column(String)  # 'above', 'below', 'crosses'
    threshold = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    triggered_at = Column(DateTime)
    
    # Relationships
    stock = relationship("Stock")


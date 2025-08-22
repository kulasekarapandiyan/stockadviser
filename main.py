from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
import uvicorn
import logging

from database import get_db, init_db
from data_fetcher import StockDataFetcher
from technical_analysis import TechnicalAnalyzer
from fundamental_analysis import FundamentalAnalyzer
from models import Stock, Portfolio, PortfolioPosition, TechnicalSignal, FundamentalScore, PricePrediction, MarketData, Alert

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Stock Advisor API",
    description="High-accuracy stock advice tool with technical and fundamental analysis",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
data_fetcher = StockDataFetcher()
technical_analyzer = TechnicalAnalyzer()
fundamental_analyzer = FundamentalAnalyzer()

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    logger.info("Stock Advisor API started successfully!")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API information"""
    return """
    <html>
        <head>
            <title>Stock Advisor API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .endpoint { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
                .method { font-weight: bold; color: #0066cc; }
                .url { font-family: monospace; background: #e0e0e0; padding: 2px 6px; border-radius: 3px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Stock Advisor API</h1>
                <p>High-accuracy stock advice tool with technical and fundamental analysis</p>
                
                <h2>Available Endpoints:</h2>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/stocks/{symbol}</span>
                    <p>Get comprehensive stock analysis including technical and fundamental data</p>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/stocks/{symbol}/technical</span>
                    <p>Get technical analysis with indicators and patterns</p>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/stocks/{symbol}/fundamental</span>
                    <p>Get fundamental analysis with scoring and metrics</p>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/stocks/{symbol}/signals</span>
                    <p>Get buy/sell signals based on combined analysis</p>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/market/overview</span>
                    <p>Get market overview and sector performance</p>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/portfolios</span>
                    <p>Get user portfolios</p>
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> <span class="url">/api/portfolios</span>
                    <p>Create new portfolio</p>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/docs</span>
                    <p>Interactive API documentation</p>
                </div>
                
                <h3>Quick Start:</h3>
                <p>Try analyzing a stock: <a href="/api/stocks/AAPL">/api/stocks/AAPL</a></p>
                <p>View API docs: <a href="/docs">/docs</a></p>
            </div>
        </body>
    </html>
    """

# Stock Analysis Endpoints
@app.get("/api/stocks/{symbol}")
async def get_stock_analysis(
    symbol: str,
    period: str = Query("1y", description="Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)"),
    interval: str = Query("1d", description="Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)"),
    db: Session = Depends(get_db)
):
    """Get comprehensive stock analysis"""
    try:
        # Fetch stock data
        stock_data = data_fetcher.get_stock_data(symbol, period, interval)
        if stock_data.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        
        # Fetch fundamental data
        fundamental_data = data_fetcher.get_fundamental_data(symbol)
        
        # Calculate technical indicators
        stock_data_with_indicators = technical_analyzer.calculate_all_indicators(stock_data)
        
        # Detect patterns
        patterns = technical_analyzer.detect_patterns(stock_data_with_indicators)
        
        # Generate technical signals
        technical_signals = technical_analyzer.generate_signals(stock_data_with_indicators)
        
        # Calculate fundamental scores
        fundamental_scores = fundamental_analyzer.calculate_fundamental_score(fundamental_data)
        
        # Generate fundamental signals
        fundamental_signals = fundamental_analyzer.generate_fundamental_signals(fundamental_data)
        
        # Combine signals for overall recommendation
        overall_signal = _combine_signals(technical_signals, fundamental_signals)
        
        return {
            "symbol": symbol,
            "period": period,
            "interval": interval,
            "last_updated": stock_data.iloc[-1]['Date'] if 'Date' in stock_data.columns else None,
            "current_price": stock_data.iloc[-1]['Close'],
            "price_change": stock_data.iloc[-1]['Close'] - stock_data.iloc[-2]['Close'] if len(stock_data) > 1 else 0,
            "price_change_percent": ((stock_data.iloc[-1]['Close'] - stock_data.iloc[-2]['Close']) / stock_data.iloc[-2]['Close'] * 100) if len(stock_data) > 1 else 0,
            "volume": stock_data.iloc[-1]['Volume'],
            "technical_analysis": {
                "indicators": stock_data_with_indicators.tail(1).to_dict('records')[0] if not stock_data_with_indicators.empty else {},
                "patterns": patterns,
                "signals": technical_signals
            },
            "fundamental_analysis": {
                "data": fundamental_data,
                "scores": fundamental_scores,
                "signals": fundamental_signals
            },
            "overall_recommendation": overall_signal
        }
        
    except HTTPException:
        # Re-raise HTTPExceptions (like 404 for no data)
        raise
    except Exception as e:
        logger.error(f"Error analyzing stock {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing stock: {str(e)}")

@app.get("/api/stocks/{symbol}/technical")
async def get_technical_analysis(
    symbol: str,
    period: str = Query("1y", description="Data period"),
    interval: str = Query("1d", description="Data interval"),
    db: Session = Depends(get_db)
):
    """Get technical analysis for a stock"""
    try:
        # Fetch stock data
        stock_data = data_fetcher.get_stock_data(symbol, period, interval)
        if stock_data.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        
        # Calculate technical indicators
        stock_data_with_indicators = technical_analyzer.calculate_all_indicators(stock_data)
        
        # Detect patterns
        patterns = technical_analyzer.detect_patterns(stock_data_with_indicators)
        
        # Generate signals
        signals = technical_analyzer.generate_signals(stock_data_with_indicators)
        
        return {
            "symbol": symbol,
            "period": period,
            "interval": interval,
            "data_points": len(stock_data),
            "indicators": stock_data_with_indicators.tail(1).to_dict('records')[0] if not stock_data_with_indicators.empty else {},
            "patterns": patterns,
            "signals": signals,
            "chart_data": stock_data_with_indicators.to_dict('records')
        }
        
    except Exception as e:
        logger.error(f"Error in technical analysis for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in technical analysis: {str(e)}")

@app.get("/api/stocks/{symbol}/fundamental")
async def get_fundamental_analysis(
    symbol: str,
    db: Session = Depends(get_db)
):
    """Get fundamental analysis for a stock"""
    try:
        # Fetch fundamental data
        fundamental_data = data_fetcher.get_fundamental_data(symbol)
        if not fundamental_data:
            raise HTTPException(status_code=404, detail=f"No fundamental data found for symbol {symbol}")
        
        # Calculate scores
        scores = fundamental_analyzer.calculate_fundamental_score(fundamental_data)
        
        # Generate signals
        signals = fundamental_analyzer.generate_fundamental_signals(fundamental_data)
        
        # Generate report
        report = fundamental_analyzer.generate_fundamental_report(fundamental_data, scores)
        
        # Get additional data
        earnings_data = data_fetcher.get_earnings_data(symbol)
        balance_sheet = data_fetcher.get_balance_sheet(symbol)
        income_statement = data_fetcher.get_income_statement(symbol)
        cash_flow = data_fetcher.get_cash_flow(symbol)
        
        return {
            "symbol": symbol,
            "company_info": {
                "name": fundamental_data.get('company_name', ''),
                "sector": fundamental_data.get('sector', ''),
                "industry": fundamental_data.get('industry', '')
            },
            "scores": scores,
            "signals": signals,
            "report": report,
            "financial_statements": {
                "earnings": earnings_data,
                "balance_sheet": balance_sheet,
                "income_statement": income_statement,
                "cash_flow": cash_flow
            },
            "key_metrics": fundamental_data
        }
        
    except Exception as e:
        logger.error(f"Error in fundamental analysis for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error in fundamental analysis: {str(e)}")

@app.get("/api/stocks/{symbol}/signals")
async def get_stock_signals(
    symbol: str,
    period: str = Query("1y", description="Data period"),
    db: Session = Depends(get_db)
):
    """Get buy/sell signals for a stock"""
    try:
        # Fetch stock data
        stock_data = data_fetcher.get_stock_data(symbol, period)
        if stock_data.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {symbol}")
        
        # Fetch fundamental data
        fundamental_data = data_fetcher.get_fundamental_data(symbol)
        
        # Calculate technical indicators and signals
        stock_data_with_indicators = technical_analyzer.calculate_all_indicators(stock_data)
        technical_signals = technical_analyzer.generate_signals(stock_data_with_indicators)
        
        # Calculate fundamental signals
        fundamental_signals = fundamental_analyzer.generate_fundamental_signals(fundamental_data)
        
        # Combine signals
        overall_signal = _combine_signals(technical_signals, fundamental_signals)
        
        return {
            "symbol": symbol,
            "technical_signals": technical_signals,
            "fundamental_signals": fundamental_signals,
            "overall_signal": overall_signal,
            "recommendation_summary": {
                "action": overall_signal.get('signal', 'hold'),
                "confidence": overall_signal.get('strength', 0),
                "reason": overall_signal.get('reason', ''),
                "last_updated": stock_data.iloc[-1]['Date'] if 'Date' in stock_data.columns else None
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting signals for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting signals: {str(e)}")

# Market Overview Endpoints
@app.get("/api/market/overview")
async def get_market_overview():
    """Get market overview and sector performance"""
    try:
        market_data = data_fetcher.get_market_overview()
        sector_data = data_fetcher.get_sector_performance()
        
        return {
            "market_indices": market_data,
            "sector_performance": sector_data,
            "last_updated": market_data.get('S&P 500', {}).get('last_updated') if market_data else None
        }
        
    except Exception as e:
        logger.error(f"Error getting market overview: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting market overview: {str(e)}")

# Portfolio Management Endpoints
@app.get("/api/portfolios")
async def get_portfolios(db: Session = Depends(get_db)):
    """Get all portfolios"""
    try:
        portfolios = db.query(Portfolio).all()
        return {"portfolios": [{"id": p.id, "name": p.name, "description": p.description} for p in portfolios]}
    except Exception as e:
        logger.error(f"Error getting portfolios: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting portfolios: {str(e)}")

@app.post("/api/portfolios")
async def create_portfolio(
    portfolio_data: dict,
    db: Session = Depends(get_db)
):
    """Create a new portfolio"""
    try:
        portfolio = Portfolio(
            name=portfolio_data.get('name'),
            description=portfolio_data.get('description', '')
        )
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
        
        return {"message": "Portfolio created successfully", "portfolio_id": portfolio.id}
        
    except Exception as e:
        logger.error(f"Error creating portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating portfolio: {str(e)}")

@app.get("/api/portfolios/{portfolio_id}")
async def get_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    """Get portfolio details with positions"""
    try:
        portfolio = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        
        positions = db.query(PortfolioPosition).filter(PortfolioPosition.portfolio_id == portfolio_id).all()
        
        portfolio_data = []
        total_value = 0
        
        for position in positions:
            stock = db.query(Stock).filter(Stock.id == position.stock_id).first()
            if stock:
                # Get current price (simplified - in production, fetch real-time data)
                current_price = 100  # Placeholder
                position_value = position.shares * current_price
                total_value += position_value
                
                portfolio_data.append({
                    "symbol": stock.symbol,
                    "company_name": stock.company_name,
                    "shares": position.shares,
                    "avg_price": position.avg_price,
                    "current_price": current_price,
                    "position_value": position_value,
                    "unrealized_pnl": position_value - (position.shares * position.avg_price)
                })
        
        return {
            "portfolio": {
                "id": portfolio.id,
                "name": portfolio.name,
                "description": portfolio.description,
                "total_value": total_value,
                "positions": portfolio_data
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting portfolio {portfolio_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting portfolio: {str(e)}")

# Utility Functions
def _combine_signals(technical_signals: Dict, fundamental_signals: Dict) -> Dict:
    """Combine technical and fundamental signals for overall recommendation"""
    try:
        # Get combined technical signal
        tech_combined = technical_signals.get('Combined', {})
        tech_signal = tech_combined.get('signal', 'hold')
        tech_strength = tech_combined.get('strength', 0.5)
        
        # Get fundamental signal
        fund_signal = fundamental_signals.get('signal', 'hold')
        fund_strength = fundamental_signals.get('strength', 0.5)
        
        # Weight the signals (technical: 60%, fundamental: 40%)
        tech_weight = 0.6
        fund_weight = 0.4
        
        # Calculate weighted score
        if tech_signal == 'buy':
            tech_score = tech_strength
        elif tech_signal == 'sell':
            tech_score = -tech_strength
        else:
            tech_score = 0
        
        if fund_signal == 'buy':
            fund_score = fund_strength
        elif fund_signal == 'sell':
            fund_score = -fund_strength
        else:
            fund_score = 0
        
        weighted_score = (tech_score * tech_weight) + (fund_score * fund_weight)
        
        # Determine final signal
        if weighted_score > 0.3:
            final_signal = 'buy'
            final_strength = min(weighted_score, 1.0)
            reason = 'Strong technical and fundamental signals'
        elif weighted_score < -0.3:
            final_signal = 'sell'
            final_strength = min(abs(weighted_score), 1.0)
            reason = 'Weak technical and fundamental signals'
        else:
            final_signal = 'hold'
            final_strength = 0.5
            reason = 'Mixed signals, maintaining position'
        
        return {
            'signal': final_signal,
            'strength': final_strength,
            'reason': reason,
            'weighted_score': weighted_score,
            'technical_contribution': tech_score * tech_weight,
            'fundamental_contribution': fund_score * fund_weight
        }
        
    except Exception as e:
        logger.error(f"Error combining signals: {str(e)}")
        return {
            'signal': 'hold',
            'strength': 0.5,
            'reason': 'Error combining signals',
            'weighted_score': 0
        }

# Health Check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Stock Advisor API"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

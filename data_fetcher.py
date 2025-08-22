import yfinance as yf
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StockDataFetcher:
    """Fetches stock data from multiple sources"""
    
    def __init__(self):
        self.alpha_vantage_key = Config.ALPHA_VANTAGE_API_KEY
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'StockAdvisor/1.0'})
    
    def get_stock_data(self, symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """Fetch stock data using yfinance"""
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                ticker = yf.Ticker(symbol)
                data = ticker.history(period=period, interval=interval)
                
                if data.empty:
                    logger.warning(f"No data found for {symbol}")
                    return pd.DataFrame()
                
                # Reset index to make date a column
                data.reset_index(inplace=True)
                data['Symbol'] = symbol
                
                return data
                
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Network error fetching {symbol} (attempt {attempt + 1}/{max_retries}): {str(e)}")
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                else:
                    logger.error(f"Failed to fetch {symbol} after {max_retries} attempts: {str(e)}")
                    return pd.DataFrame()
            except Exception as e:
                logger.error(f"Error fetching data for {symbol}: {str(e)}")
                return pd.DataFrame()
    
    def get_fundamental_data(self, symbol: str) -> Dict:
        """Fetch fundamental data for a stock"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get basic info
            info = ticker.info
            
            fundamental_data = {
                'symbol': symbol,
                'company_name': info.get('longName', ''),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'pb_ratio': info.get('priceToBook', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'beta': info.get('beta', 0),
                'roe': info.get('returnOnEquity', 0),
                'roa': info.get('returnOnAssets', 0),
                'debt_to_equity': info.get('debtToEquity', 0),
                'current_ratio': info.get('currentRatio', 0),
                'quick_ratio': info.get('quickRatio', 0),
                'gross_margin': info.get('grossMargins', 0),
                'operating_margin': info.get('operatingMargins', 0),
                'net_margin': info.get('netIncomeToCommon', 0),
                'revenue_growth': info.get('revenueGrowth', 0),
                'earnings_growth': info.get('earningsGrowth', 0),
                'book_value': info.get('bookValue', 0),
                'cash_per_share': info.get('totalCashPerShare', 0),
                'revenue_per_share': info.get('revenuePerShare', 0),
                'earnings_per_share': info.get('trailingEps', 0),
                'forward_pe': info.get('forwardPE', 0),
                'peg_ratio': info.get('pegRatio', 0),
                'price_to_sales': info.get('priceToSalesTrailing12Months', 0),
                'enterprise_value': info.get('enterpriseValue', 0),
                'enterprise_to_revenue': info.get('enterpriseToRevenue', 0),
                'enterprise_to_ebitda': info.get('enterpriseToEbitda', 0),
                'shares_outstanding': info.get('sharesOutstanding', 0),
                'float_shares': info.get('floatShares', 0),
                'insider_ownership': info.get('heldPercentInsiders', 0),
                'institutional_ownership': info.get('heldPercentInstitutions', 0),
                'short_ratio': info.get('shortRatio', 0),
                'short_percent_of_float': info.get('shortPercentOfFloat', 0),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 0),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow', 0),
                'fifty_day_average': info.get('fiftyDayAverage', 0),
                'two_hundred_day_average': info.get('twoHundredDayAverage', 0),
                'volume': info.get('volume', 0),
                'avg_volume': info.get('averageVolume', 0),
                'last_updated': datetime.now()
            }
            
            return fundamental_data
            
        except Exception as e:
            logger.error(f"Error fetching fundamental data for {symbol}: {str(e)}")
            return {}
    
    def get_earnings_data(self, symbol: str) -> Dict:
        """Fetch earnings data for a stock"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get earnings
            earnings = ticker.earnings
            quarterly_earnings = ticker.quarterly_earnings
            
            earnings_data = {
                'symbol': symbol,
                'annual_earnings': earnings.to_dict('records') if not earnings.empty else [],
                'quarterly_earnings': quarterly_earnings.to_dict('records') if not quarterly_earnings.empty else [],
                'last_updated': datetime.now()
            }
            
            return earnings_data
            
        except Exception as e:
            logger.error(f"Error fetching earnings data for {symbol}: {str(e)}")
            return {}
    
    def get_balance_sheet(self, symbol: str) -> Dict:
        """Fetch balance sheet data"""
        try:
            ticker = yf.Ticker(symbol)
            balance_sheet = ticker.balance_sheet
            
            if balance_sheet.empty:
                return {}
            
            return {
                'symbol': symbol,
                'balance_sheet': balance_sheet.to_dict('records'),
                'last_updated': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error fetching balance sheet for {symbol}: {str(e)}")
            return {}
    
    def get_income_statement(self, symbol: str) -> Dict:
        """Fetch income statement data"""
        try:
            ticker = yf.Ticker(symbol)
            income_stmt = ticker.income_stmt
            
            if income_stmt.empty:
                return {}
            
            return {
                'symbol': symbol,
                'income_statement': income_stmt.to_dict('records'),
                'last_updated': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error fetching income statement for {symbol}: {str(e)}")
            return {}
    
    def get_cash_flow(self, symbol: str) -> Dict:
        """Fetch cash flow data"""
        try:
            ticker = yf.Ticker(symbol)
            cash_flow = ticker.cashflow
            
            if cash_flow.empty:
                return {}
            
            return {
                'symbol': symbol,
                'cash_flow': cash_flow.to_dict('records'),
                'last_updated': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error fetching cash flow for {symbol}: {str(e)}")
            return {}
    
    def get_analyst_recommendations(self, symbol: str) -> Dict:
        """Fetch analyst recommendations"""
        try:
            ticker = yf.Ticker(symbol)
            recommendations = ticker.recommendations
            
            if recommendations.empty:
                return {}
            
            return {
                'symbol': symbol,
                'recommendations': recommendations.to_dict('records'),
                'last_updated': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error fetching analyst recommendations for {symbol}: {str(e)}")
            return {}
    
    def get_market_sentiment(self, symbol: str) -> Dict:
        """Fetch market sentiment data"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get various sentiment indicators
            sentiment_data = {
                'symbol': symbol,
                'recommendations_mean': ticker.recommendations_mean if hasattr(ticker, 'recommendations_mean') else None,
                'recommendations_summary': ticker.recommendations_summary if hasattr(ticker, 'recommendations_summary') else None,
                'major_holders': ticker.major_holders.to_dict('records') if hasattr(ticker, 'major_holders') and not ticker.major_holders.empty else [],
                'institutional_holders': ticker.institutional_holders.to_dict('records') if hasattr(ticker, 'institutional_holders') and not ticker.institutional_holders.empty else [],
                'last_updated': datetime.now()
            }
            
            return sentiment_data
            
        except Exception as e:
            logger.error(f"Error fetching market sentiment for {symbol}: {str(e)}")
            return {}
    
    def get_news_data(self, symbol: str, limit: int = 10) -> List[Dict]:
        """Fetch news data for a stock"""
        try:
            ticker = yf.Ticker(symbol)
            news = ticker.news
            
            if not news:
                return []
            
            # Limit the number of news items
            limited_news = news[:limit]
            
            news_data = []
            for item in limited_news:
                news_data.append({
                    'symbol': symbol,
                    'title': item.get('title', ''),
                    'summary': item.get('summary', ''),
                    'link': item.get('link', ''),
                    'publisher': item.get('publisher', ''),
                    'published': item.get('providerPublishTime', ''),
                    'last_updated': datetime.now()
                })
            
            return news_data
            
        except Exception as e:
            logger.error(f"Error fetching news for {symbol}: {str(e)}")
            return []
    
    def get_sector_performance(self) -> Dict:
        """Fetch sector performance data"""
        try:
            # Get sector ETFs for performance comparison
            sector_etfs = {
                'XLK': 'Technology',
                'XLF': 'Financials',
                'XLE': 'Energy',
                'XLV': 'Healthcare',
                'XLI': 'Industrials',
                'XLP': 'Consumer Staples',
                'XLY': 'Consumer Discretionary',
                'XLB': 'Materials',
                'XLU': 'Utilities',
                'XLRE': 'Real Estate'
            }
            
            sector_data = {}
            for etf, sector in sector_etfs.items():
                try:
                    data = self.get_stock_data(etf, period="1y")
                    if not data.empty:
                        # Calculate YTD return
                        ytd_return = ((data.iloc[-1]['Close'] - data.iloc[0]['Close']) / data.iloc[0]['Close']) * 100
                        sector_data[sector] = {
                            'etf': etf,
                            'ytd_return': ytd_return,
                            'current_price': data.iloc[-1]['Close'],
                            'volume': data.iloc[-1]['Volume']
                        }
                except Exception as e:
                    logger.warning(f"Error fetching data for {etf}: {str(e)}")
                    continue
            
            return sector_data
            
        except Exception as e:
            logger.error(f"Error fetching sector performance: {str(e)}")
            return {}
    
    def get_market_overview(self) -> Dict:
        """Get overall market overview"""
        try:
            # Get major indices
            indices = {
                '^GSPC': 'S&P 500',
                '^DJI': 'Dow Jones',
                '^IXIC': 'NASDAQ',
                '^VIX': 'VIX Volatility'
            }
            
            market_data = {}
            for symbol, name in indices.items():
                try:
                    data = self.get_stock_data(symbol, period="1d")
                    if not data.empty:
                        market_data[name] = {
                            'symbol': symbol,
                            'current_value': data.iloc[-1]['Close'],
                            'change': data.iloc[-1]['Close'] - data.iloc[-1]['Open'],
                            'change_percent': ((data.iloc[-1]['Close'] - data.iloc[-1]['Open']) / data.iloc[-1]['Open']) * 100,
                            'volume': data.iloc[-1]['Volume']
                        }
                except Exception as e:
                    logger.warning(f"Error fetching data for {symbol}: {str(e)}")
                    continue
            
            return market_data
            
        except Exception as e:
            logger.error(f"Error fetching market overview: {str(e)}")
            return {}
    
    def batch_fetch_data(self, symbols: List[str], data_types: List[str] = None) -> Dict:
        """Fetch multiple types of data for multiple symbols"""
        if data_types is None:
            data_types = ['price', 'fundamental', 'earnings']
        
        results = {}
        
        for symbol in symbols:
            results[symbol] = {}
            
            if 'price' in data_types:
                results[symbol]['price'] = self.get_stock_data(symbol)
            
            if 'fundamental' in data_types:
                results[symbol]['fundamental'] = self.get_fundamental_data(symbol)
            
            if 'earnings' in data_types:
                results[symbol]['earnings'] = self.get_earnings_data(symbol)
            
            # Add delay to avoid rate limiting
            time.sleep(0.1)
        
        return results


import pandas as pd
import numpy as np
# import talib  # Commented out - requires special installation
try:
    import talib
    TALIB_AVAILABLE = True
except ImportError:
    TALIB_AVAILABLE = False
    print("Warning: talib not available. Using alternative technical analysis methods.")
from typing import Dict, List, Tuple, Optional
import logging
from config import Config

logger = logging.getLogger(__name__)

class TechnicalAnalyzer:
    """Comprehensive technical analysis for stocks"""
    
    def __init__(self):
        self.rsi_period = Config.RSI_PERIOD
        self.macd_fast = Config.MACD_FAST
        self.macd_slow = Config.MACD_SLOW
        self.macd_signal = Config.MACD_SIGNAL
        self.bollinger_period = Config.BOLLINGER_PERIOD
        self.bollinger_std = Config.BOLLINGER_STD
    
    def calculate_all_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate all technical indicators for the dataset"""
        if data.empty:
            return data
        
        try:
            # Ensure we have required columns
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in required_cols:
                if col not in data.columns:
                    logger.error(f"Missing required column: {col}")
                    return data
            
            # Calculate basic indicators
            data = self._calculate_moving_averages(data)
            data = self._calculate_rsi(data)
            data = self._calculate_macd(data)
            data = self._calculate_bollinger_bands(data)
            data = self._calculate_stochastic(data)
            data = self._calculate_williams_r(data)
            data = self._calculate_atr(data)
            data = self._calculate_volume_indicators(data)
            data = self._calculate_momentum_indicators(data)
            data = self._calculate_trend_indicators(data)
            
            return data
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {str(e)}")
            return data
    
    def _calculate_moving_averages(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate various moving averages"""
        try:
            # Simple Moving Averages
            data['SMA_5'] = data['Close'].rolling(window=5).mean()
            data['SMA_10'] = data['Close'].rolling(window=10).mean()
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            data['SMA_50'] = data['Close'].rolling(window=50).mean()
            data['SMA_100'] = data['Close'].rolling(window=100).mean()
            data['SMA_200'] = data['Close'].rolling(window=200).mean()
            
            # Exponential Moving Averages
            data['EMA_12'] = data['Close'].ewm(span=12).mean()
            data['EMA_26'] = data['Close'].ewm(span=26).mean()
            data['EMA_50'] = data['Close'].ewm(span=50).mean()
            data['EMA_200'] = data['Close'].ewm(span=200).mean()
            
            # Weighted Moving Average (simplified)
            data['WMA_20'] = data['Close'].rolling(window=20).apply(
                lambda x: np.average(x, weights=np.arange(1, len(x) + 1)))
            
        except Exception as e:
            logger.error(f"Error calculating moving averages: {str(e)}")
        
        return data
    
    def _calculate_rsi(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate RSI indicator"""
        try:
            if TALIB_AVAILABLE:
                data['RSI'] = talib.RSI(data['Close'], timeperiod=self.rsi_period)
            else:
                # Manual RSI calculation
                delta = data['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()
                rs = gain / loss
                data['RSI'] = 100 - (100 / (1 + rs))
            
            data['RSI_Overbought'] = 70
            data['RSI_Oversold'] = 30
        except Exception as e:
            logger.error(f"Error calculating RSI: {str(e)}")
        
        return data
    
    def _calculate_macd(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate MACD indicator"""
        try:
            if TALIB_AVAILABLE:
                macd, macd_signal, macd_hist = talib.MACD(
                    data['Close'], 
                    fastperiod=self.macd_fast, 
                    slowperiod=self.macd_slow, 
                    signalperiod=self.macd_signal
                )
            else:
                # Manual MACD calculation
                ema_fast = data['Close'].ewm(span=self.macd_fast).mean()
                ema_slow = data['Close'].ewm(span=self.macd_slow).mean()
                macd = ema_fast - ema_slow
                macd_signal = macd.ewm(span=self.macd_signal).mean()
                macd_hist = macd - macd_signal
            
            data['MACD'] = macd
            data['MACD_Signal'] = macd_signal
            data['MACD_Histogram'] = macd_hist
            
        except Exception as e:
            logger.error(f"Error calculating MACD: {str(e)}")
        
        return data
    
    def _calculate_bollinger_bands(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate Bollinger Bands"""
        try:
            if TALIB_AVAILABLE:
                upper, middle, lower = talib.BBANDS(
                    data['Close'], 
                    timeperiod=self.bollinger_period, 
                    nbdevup=self.bollinger_std, 
                    nbdevdn=self.bollinger_std
                )
            else:
                # Manual Bollinger Bands calculation
                middle = data['Close'].rolling(window=self.bollinger_period).mean()
                std = data['Close'].rolling(window=self.bollinger_period).std()
                upper = middle + (std * self.bollinger_std)
                lower = middle - (std * self.bollinger_std)
            
            data['BB_Upper'] = upper
            data['BB_Middle'] = middle
            data['BB_Lower'] = lower
            data['BB_Width'] = (upper - lower) / middle
            data['BB_Position'] = (data['Close'] - lower) / (upper - lower)
            
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {str(e)}")
        
        return data
    
    def _calculate_stochastic(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate Stochastic Oscillator"""
        try:
            if TALIB_AVAILABLE:
                slowk, slowd = talib.STOCH(
                    data['High'], data['Low'], data['Close'],
                    fastk_period=14, slowk_period=3, slowd_period=3
                )
            else:
                # Manual Stochastic calculation
                low_min = data['Low'].rolling(window=14).min()
                high_max = data['High'].rolling(window=14).max()
                slowk = 100 * ((data['Close'] - low_min) / (high_max - low_min))
                slowd = slowk.rolling(window=3).mean()
            
            data['Stoch_K'] = slowk
            data['Stoch_D'] = slowd
            
        except Exception as e:
            logger.error(f"Error calculating Stochastic: {str(e)}")
        
        return data
    
    def _calculate_williams_r(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate Williams %R"""
        try:
            if TALIB_AVAILABLE:
                data['Williams_R'] = talib.WILLR(data['High'], data['Low'], data['Close'], timeperiod=14)
            else:
                # Manual Williams %R calculation
                high_max = data['High'].rolling(window=14).max()
                low_min = data['Low'].rolling(window=14).min()
                data['Williams_R'] = -100 * ((high_max - data['Close']) / (high_max - low_min))
            
        except Exception as e:
            logger.error(f"Error calculating Williams %R: {str(e)}")
        
        return data
    
    def _calculate_atr(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate Average True Range"""
        try:
            if TALIB_AVAILABLE:
                data['ATR'] = talib.ATR(data['High'], data['Low'], data['Close'], timeperiod=14)
            else:
                # Manual ATR calculation
                high_low = data['High'] - data['Low']
                high_close = np.abs(data['High'] - data['Close'].shift())
                low_close = np.abs(data['Low'] - data['Close'].shift())
                true_range = np.maximum(high_low, np.maximum(high_close, low_close))
                data['ATR'] = true_range.rolling(window=14).mean()
            
        except Exception as e:
            logger.error(f"Error calculating ATR: {str(e)}")
        
        return data
    
    def _calculate_volume_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate volume-based indicators"""
        try:
            # On-Balance Volume (OBV)
            data['OBV'] = (np.sign(data['Close'].diff()) * data['Volume']).fillna(0).cumsum()
            
            # Volume Weighted Average Price (VWAP)
            data['VWAP'] = (data['Close'] * data['Volume']).cumsum() / data['Volume'].cumsum()
            
            # Money Flow Index (MFI)
            typical_price = (data['High'] + data['Low'] + data['Close']) / 3
            money_flow = typical_price * data['Volume']
            
            positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0).rolling(window=14).sum()
            negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0).rolling(window=14).sum()
            
            money_ratio = positive_flow / negative_flow
            data['MFI'] = 100 - (100 / (1 + money_ratio))
            
        except Exception as e:
            logger.error(f"Error calculating volume indicators: {str(e)}")
        
        return data
    
    def _calculate_momentum_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate momentum indicators"""
        try:
            # Rate of Change (ROC)
            data['ROC'] = ((data['Close'] - data['Close'].shift(10)) / data['Close'].shift(10)) * 100
            
            # Momentum
            data['Momentum'] = data['Close'] - data['Close'].shift(10)
            
            # Commodity Channel Index (CCI)
            typical_price = (data['High'] + data['Low'] + data['Close']) / 3
            sma_tp = typical_price.rolling(window=20).mean()
            mean_deviation = np.abs(typical_price - sma_tp).rolling(window=20).mean()
            data['CCI'] = (typical_price - sma_tp) / (0.015 * mean_deviation)
            
        except Exception as e:
            logger.error(f"Error calculating momentum indicators: {str(e)}")
        
        return data
    
    def _calculate_trend_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate trend indicators"""
        try:
            # Average Directional Index (ADX)
            if TALIB_AVAILABLE:
                data['ADX'] = talib.ADX(data['High'], data['Low'], data['Close'], timeperiod=14)
            else:
                # Simplified ADX calculation
                data['ADX'] = data['Close'].rolling(window=14).std()
            
            # Parabolic SAR (simplified)
            data['SAR'] = data['Low'].rolling(window=5).min()
            
            # Directional Indicators
            data['DI_Plus'] = data['Close'].diff().rolling(window=14).apply(
                lambda x: x[x > 0].sum() / len(x) if len(x) > 0 else 0
            )
            data['DI_Minus'] = data['Close'].diff().rolling(window=14).apply(
                lambda x: abs(x[x < 0].sum()) / len(x) if len(x) > 0 else 0
            )
            
        except Exception as e:
            logger.error(f"Error calculating trend indicators: {str(e)}")
        
        return data
    
    def detect_patterns(self, data: pd.DataFrame) -> Dict[str, List[Dict]]:
        """Detect various candlestick and chart patterns"""
        if data.empty:
            return {}
        
        patterns = {}
        
        try:
            # Candlestick patterns
            candlestick_patterns = self._detect_candlestick_patterns(data)
            patterns['candlestick'] = candlestick_patterns
            
            # Chart patterns
            chart_patterns = self._detect_chart_patterns(data)
            patterns['chart'] = chart_patterns
            
            # Support and resistance
            support_resistance = self._detect_support_resistance(data)
            patterns['support_resistance'] = support_resistance
            
        except Exception as e:
            logger.error(f"Error detecting patterns: {str(e)}")
        
        return patterns
    
    def _detect_candlestick_patterns(self, data: pd.DataFrame) -> List[Dict]:
        """Detect candlestick patterns using TA-Lib"""
        patterns = []
        
        try:
            # List of candlestick patterns to detect
            pattern_functions = {
                'CDL2CROWS': 'Two Crows',
                'CDL3BLACKCROWS': 'Three Black Crows',
                'CDL3INSIDE': 'Three Inside Up/Down',
                'CDL3LINESTRIKE': 'Three-Line Strike',
                'CDL3OUTSIDE': 'Three Outside Up/Down',
                'CDL3STARSINSOUTH': 'Three Stars In The South',
                'CDL3WHITESOLDIERS': 'Three White Soldiers',
                'CDLABANDONEDBABY': 'Abandoned Baby',
                'CDLADVANCEBLOCK': 'Advance Block',
                'CDLBELTHOLD': 'Belt-hold',
                'CDLBREAKAWAY': 'Breakaway',
                'CDLDARKCLOUDCOVER': 'Dark Cloud Cover',
                'CDLDOJI': 'Doji',
                'CDLDOJISTAR': 'Doji Star',
                'CDLDRAGONFLYDOJI': 'Dragonfly Doji',
                'CDLENGULFING': 'Engulfing Pattern',
                'CDLEVENINGDOJISTAR': 'Evening Doji Star',
                'CDLEVENINGSTAR': 'Evening Star',
                'CDLGAPSIDESIDEWHITE': 'Up/Down-gap side-by-side white lines',
                'CDLGRAVESTONEDOJI': 'Gravestone Doji',
                'CDLHAMMER': 'Hammer',
                'CDLHANGINGMAN': 'Hanging Man',
                'CDLHARAMI': 'Harami Pattern',
                'CDLHARAMICROSS': 'Harami Cross Pattern',
                'CDLHIGHWAVE': 'High-Wave Candle',
                'CDLHIKKAKE': 'Hikkake Pattern',
                'CDLHIKKAKEMOD': 'Modified Hikkake Pattern',
                'CDLHOMINGPIGEON': 'Homing Pigeon',
                'CDLIDENTICAL3CROWS': 'Identical Three Crows',
                'CDLINNECK': 'In-Neck Pattern',
                'CDLINVERTEDHAMMER': 'Inverted Hammer',
                'CDLKICKING': 'Kicking',
                'CDLKICKINGBYLENGTH': 'Kicking - bull/bear determined by the longer marubozu',
                'CDLLADDERBOTTOM': 'Ladder Bottom',
                'CDLLONGLEGGEDDOJI': 'Long Legged Doji',
                'CDLLONGLINE': 'Long Line Candle',
                'CDLMARUBOZU': 'Marubozu',
                'CDLMATCHINGLOW': 'Matching Low',
                'CDLMATHOLD': 'Mat Hold',
                'CDLMORNINGDOJISTAR': 'Morning Doji Star',
                'CDLMORNINGSTAR': 'Morning Star',
                'CDLONNECK': 'On-Neck Pattern',
                'CDLPIERCING': 'Piercing Pattern',
                'CDLRICKSHAWMAN': 'Rickshaw Man',
                'CDLRISEFALL3METHODS': 'Rising/Falling Three Methods',
                'CDLSEPARATINGLINES': 'Separating Lines',
                'CDLSHOOTINGSTAR': 'Shooting Star',
                'CDLSHORTLINE': 'Short Line Candle',
                'CDLSPINNINGTOP': 'Spinning Top',
                'CDLSTALLEDPATTERN': 'Stalled Pattern',
                'CDLSTICKSANDWICH': 'Stick Sandwich',
                'CDLTAKURI': 'Takuri (Dragonfly Doji with very long lower shadow)',
                'CDLTASUKIGAP': 'Tasuki Gap',
                'CDLTHRUSTING': 'Thrusting Pattern',
                'CDLTRISTAR': 'Tristar Pattern',
                'CDLUNIQUE3RIVER': 'Unique 3 River',
                'CDLUPSIDEGAP2CROWS': 'Upside Gap Two Crows',
                'CDLXSIDEGAP3METHODS': 'Upside/Downside Gap Three Methods'
            }
            
            for pattern_func, pattern_name in pattern_functions.items():
                try:
                    if hasattr(talib, pattern_func):
                        func = getattr(talib, pattern_func)
                        result = func(data['Open'], data['High'], data['Low'], data['Close'])
                        
                        # Find where pattern occurs (non-zero values)
                        pattern_occurrences = np.where(result != 0)[0]
                        
                        for idx in pattern_occurrences:
                            if idx < len(data):
                                patterns.append({
                                    'pattern': pattern_name,
                                    'date': data.iloc[idx]['Date'] if 'Date' in data.columns else idx,
                                    'value': result[idx],
                                    'strength': abs(result[idx]),
                                    'type': 'bullish' if result[idx] > 0 else 'bearish'
                                })
                except Exception as e:
                    logger.debug(f"Error detecting pattern {pattern_name}: {str(e)}")
                    continue
            
        except Exception as e:
            logger.error(f"Error in candlestick pattern detection: {str(e)}")
        
        return patterns
    
    def _detect_chart_patterns(self, data: pd.DataFrame) -> List[Dict]:
        """Detect chart patterns like head and shoulders, triangles, etc."""
        patterns = []
        
        try:
            # Head and Shoulders detection
            hs_patterns = self._detect_head_and_shoulders(data)
            patterns.extend(hs_patterns)
            
            # Triangle detection
            triangle_patterns = self._detect_triangles(data)
            patterns.extend(triangle_patterns)
            
            # Double top/bottom detection
            double_patterns = self._detect_double_patterns(data)
            patterns.extend(double_patterns)
            
        except Exception as e:
            logger.error(f"Error in chart pattern detection: {str(e)}")
        
        return patterns
    
    def _detect_head_and_shoulders(self, data: pd.DataFrame) -> List[Dict]:
        """Detect head and shoulders pattern"""
        patterns = []
        
        try:
            if len(data) < 20:
                return patterns
            
            # Look for potential head and shoulders pattern
            for i in range(10, len(data) - 10):
                # Check for left shoulder
                left_shoulder = data.iloc[i-5:i].max()
                left_shoulder_idx = data.iloc[i-5:i]['High'].idxmax()
                
                # Check for head
                head = data.iloc[i:i+5].max()
                head_idx = data.iloc[i:i+5]['High'].idxmax()
                
                # Check for right shoulder
                right_shoulder = data.iloc[i+5:i+10].max()
                right_shoulder_idx = data.iloc[i+5:i+10]['High'].idxmax()
                
                # Check if head is higher than shoulders
                if (head['High'] > left_shoulder['High'] and 
                    head['High'] > right_shoulder['High'] and
                    abs(left_shoulder['High'] - right_shoulder['High']) / left_shoulder['High'] < 0.1):
                    
                    patterns.append({
                        'pattern': 'Head and Shoulders',
                        'date': data.iloc[head_idx]['Date'] if 'Date' in data.columns else head_idx,
                        'type': 'bearish',
                        'strength': 0.8,
                        'left_shoulder': left_shoulder['High'],
                        'head': head['High'],
                        'right_shoulder': right_shoulder['High']
                    })
            
        except Exception as e:
            logger.error(f"Error detecting head and shoulders: {str(e)}")
        
        return patterns
    
    def _detect_triangles(self, data: pd.DataFrame) -> List[Dict]:
        """Detect triangle patterns"""
        patterns = []
        
        try:
            if len(data) < 20:
                return patterns
            
            # Look for triangle patterns over the last 20 periods
            recent_data = data.tail(20)
            
            # Calculate trend lines
            highs = recent_data['High'].values
            lows = recent_data['Low'].values
            dates = range(len(recent_data))
            
            # Fit lines to highs and lows
            high_slope, high_intercept = np.polyfit(dates, highs, 1)
            low_slope, low_intercept = np.polyfit(dates, lows, 1)
            
            # Check for triangle patterns
            if abs(high_slope) < 0.1 and abs(low_slope) < 0.1:
                # Horizontal triangle
                pattern_type = 'Rectangle'
            elif high_slope < -0.1 and low_slope > 0.1:
                # Ascending triangle
                pattern_type = 'Ascending Triangle'
            elif high_slope < -0.1 and low_slope < -0.1:
                # Descending triangle
                pattern_type = 'Descending Triangle'
            elif high_slope < -0.1 and abs(low_slope) < 0.1:
                # Descending triangle
                pattern_type = 'Descending Triangle'
            elif abs(high_slope) < 0.1 and low_slope > 0.1:
                # Ascending triangle
                pattern_type = 'Ascending Triangle'
            else:
                return patterns
            
            patterns.append({
                'pattern': pattern_type,
                'date': data.iloc[-1]['Date'] if 'Date' in data.columns else len(data) - 1,
                'type': 'neutral',
                'strength': 0.6,
                'high_slope': high_slope,
                'low_slope': low_slope
            })
            
        except Exception as e:
            logger.error(f"Error detecting triangles: {str(e)}")
        
        return patterns
    
    def _detect_double_patterns(self, data: pd.DataFrame) -> List[Dict]:
        """Detect double top and double bottom patterns"""
        patterns = []
        
        try:
            if len(data) < 20:
                return patterns
            
            # Look for double patterns over the last 20 periods
            recent_data = data.tail(20)
            
            # Find local peaks and troughs
            highs = recent_data['High'].values
            lows = recent_data['Low'].values
            
            # Simple peak detection
            peaks = []
            troughs = []
            
            for i in range(1, len(highs) - 1):
                if highs[i] > highs[i-1] and highs[i] > highs[i+1]:
                    peaks.append((i, highs[i]))
                if lows[i] < lows[i-1] and lows[i] < lows[i+1]:
                    troughs.append((i, lows[i]))
            
            # Check for double top
            if len(peaks) >= 2:
                peak1, peak2 = peaks[-2], peaks[-1]
                if abs(peak1[1] - peak2[1]) / peak1[1] < 0.05:  # Within 5%
                    patterns.append({
                        'pattern': 'Double Top',
                        'date': data.iloc[-1]['Date'] if 'Date' in data.columns else len(data) - 1,
                        'type': 'bearish',
                        'strength': 0.7,
                        'peak1': peak1[1],
                        'peak2': peak2[1]
                    })
            
            # Check for double bottom
            if len(troughs) >= 2:
                trough1, trough2 = troughs[-2], troughs[-1]
                if abs(trough1[1] - trough2[1]) / trough1[1] < 0.05:  # Within 5%
                    patterns.append({
                        'pattern': 'Double Bottom',
                        'date': data.iloc[-1]['Date'] if 'Date' in data.columns else len(data) - 1,
                        'type': 'bullish',
                        'strength': 0.7,
                        'trough1': trough1[1],
                        'trough2': trough2[1]
                    })
            
        except Exception as e:
            logger.error(f"Error detecting double patterns: {str(e)}")
        
        return patterns
    
    def _detect_support_resistance(self, data: pd.DataFrame) -> List[Dict]:
        """Detect support and resistance levels"""
        levels = []
        
        try:
            if len(data) < 20:
                return levels
            
            # Use recent data for level detection
            recent_data = data.tail(50)
            highs = recent_data['High'].values
            lows = recent_data['Low'].values
            
            # Find significant levels using clustering
            from sklearn.cluster import DBSCAN
            
            # Combine highs and lows for clustering
            all_levels = np.concatenate([highs, lows])
            all_levels = all_levels.reshape(-1, 1)
            
            # Cluster levels that are close to each other
            clustering = DBSCAN(eps=0.02, min_samples=3).fit(all_levels)
            
            # Get cluster centers
            unique_labels = np.unique(clustering.labels_)
            for label in unique_labels:
                if label != -1:  # Skip noise points
                    cluster_points = all_levels[clustering.labels_ == label]
                    center = np.mean(cluster_points)
                    
                    # Determine if it's support or resistance
                    current_price = data.iloc[-1]['Close']
                    level_type = 'resistance' if center > current_price else 'support'
                    
                    levels.append({
                        'pattern': f'{level_type.title()} Level',
                        'date': data.iloc[-1]['Date'] if 'Date' in data.columns else len(data) - 1,
                        'type': 'neutral',
                        'strength': 0.8,
                        'level': center,
                        'level_type': level_type,
                        'cluster_size': len(cluster_points)
                    })
            
        except Exception as e:
            logger.error(f"Error detecting support/resistance: {str(e)}")
        
        return levels
    
    def generate_signals(self, data: pd.DataFrame) -> Dict[str, Dict]:
        """Generate buy/sell signals based on technical indicators"""
        if data.empty:
            return {}
        
        signals = {}
        
        try:
            # RSI signals
            if 'RSI' in data.columns:
                signals['RSI'] = self._generate_rsi_signals(data)
            
            # MACD signals
            if 'MACD' in data.columns and 'MACD_Signal' in data.columns:
                signals['MACD'] = self._generate_macd_signals(data)
            
            # Bollinger Bands signals
            if 'BB_Upper' in data.columns and 'BB_Lower' in data.columns:
                signals['Bollinger_Bands'] = self._generate_bollinger_signals(data)
            
            # Moving Average signals
            if 'SMA_20' in data.columns and 'SMA_50' in data.columns:
                signals['Moving_Averages'] = self._generate_ma_signals(data)
            
            # Volume signals
            if 'OBV' in data.columns and 'Volume' in data.columns:
                signals['Volume'] = self._generate_volume_signals(data)
            
            # Combined signal
            signals['Combined'] = self._generate_combined_signal(signals)
            
        except Exception as e:
            logger.error(f"Error generating signals: {str(e)}")
        
        return signals
    
    def _generate_rsi_signals(self, data: pd.DataFrame) -> Dict:
        """Generate RSI-based signals"""
        latest_rsi = data['RSI'].iloc[-1]
        
        if pd.isna(latest_rsi):
            return {'signal': 'neutral', 'strength': 0, 'reason': 'Insufficient data'}
        
        if latest_rsi > 70:
            signal = 'sell'
            strength = min((latest_rsi - 70) / 30, 1.0)
            reason = f'RSI overbought at {latest_rsi:.2f}'
        elif latest_rsi < 30:
            signal = 'buy'
            strength = min((30 - latest_rsi) / 30, 1.0)
            reason = f'RSI oversold at {latest_rsi:.2f}'
        else:
            signal = 'hold'
            strength = 0.5
            reason = f'RSI neutral at {latest_rsi:.2f}'
        
        return {
            'signal': signal,
            'strength': strength,
            'reason': reason,
            'value': latest_rsi
        }
    
    def _generate_macd_signals(self, data: pd.DataFrame) -> Dict:
        """Generate MACD-based signals"""
        latest_macd = data['MACD'].iloc[-1]
        latest_signal = data['MACD_Signal'].iloc[-1]
        latest_hist = data['MACD_Histogram'].iloc[-1]
        
        if pd.isna(latest_macd) or pd.isna(latest_signal):
            return {'signal': 'neutral', 'strength': 0, 'reason': 'Insufficient data'}
        
        # MACD crossover signals
        if latest_macd > latest_signal and data['MACD'].iloc[-2] <= data['MACD_Signal'].iloc[-2]:
            signal = 'buy'
            strength = min(abs(latest_hist) / 2, 1.0)
            reason = 'MACD bullish crossover'
        elif latest_macd < latest_signal and data['MACD'].iloc[-2] >= data['MACD_Signal'].iloc[-2]:
            signal = 'sell'
            strength = min(abs(latest_hist) / 2, 1.0)
            reason = 'MACD bearish crossover'
        else:
            signal = 'hold'
            strength = 0.5
            reason = 'MACD no crossover'
        
        return {
            'signal': signal,
            'strength': strength,
            'reason': reason,
            'macd': latest_macd,
            'signal_line': latest_signal,
            'histogram': latest_hist
        }
    
    def _generate_bollinger_signals(self, data: pd.DataFrame) -> Dict:
        """Generate Bollinger Bands-based signals"""
        latest_close = data['Close'].iloc[-1]
        latest_upper = data['BB_Upper'].iloc[-1]
        latest_lower = data['BB_Lower'].iloc[-1]
        latest_position = data['BB_Position'].iloc[-1]
        
        if pd.isna(latest_close) or pd.isna(latest_upper) or pd.isna(latest_lower):
            return {'signal': 'neutral', 'strength': 0, 'reason': 'Insufficient data'}
        
        if latest_close <= latest_lower:
            signal = 'buy'
            strength = min((latest_lower - latest_close) / latest_lower * 10, 1.0)
            reason = 'Price at or below lower Bollinger Band'
        elif latest_close >= latest_upper:
            signal = 'sell'
            strength = min((latest_close - latest_upper) / latest_upper * 10, 1.0)
            reason = 'Price at or above upper Bollinger Band'
        else:
            signal = 'hold'
            strength = 0.5
            reason = f'Price within Bollinger Bands (position: {latest_position:.2f})'
        
        return {
            'signal': signal,
            'strength': strength,
            'reason': reason,
            'position': latest_position,
            'upper_band': latest_upper,
            'lower_band': latest_lower
        }
    
    def _generate_ma_signals(self, data: pd.DataFrame) -> Dict:
        """Generate Moving Average-based signals"""
        latest_close = data['Close'].iloc[-1]
        latest_sma20 = data['SMA_20'].iloc[-1]
        latest_sma50 = data['SMA_50'].iloc[-1]
        latest_sma200 = data['SMA_200'].iloc[-1]
        
        if pd.isna(latest_sma20) or pd.isna(latest_sma50):
            return {'signal': 'neutral', 'strength': 0, 'reason': 'Insufficient data'}
        
        # Golden Cross / Death Cross
        if latest_sma20 > latest_sma50 and data['SMA_20'].iloc[-2] <= data['SMA_50'].iloc[-2]:
            signal = 'buy'
            strength = 0.8
            reason = 'Golden Cross (20 SMA crosses above 50 SMA)'
        elif latest_sma20 < latest_sma50 and data['SMA_20'].iloc[-2] >= data['SMA_50'].iloc[-2]:
            signal = 'sell'
            strength = 0.8
            reason = 'Death Cross (20 SMA crosses below 50 SMA)'
        else:
            signal = 'hold'
            strength = 0.5
            reason = 'No MA crossover'
        
        # Trend analysis
        trend = 'bullish' if latest_close > latest_sma200 else 'bearish'
        
        return {
            'signal': signal,
            'strength': strength,
            'reason': reason,
            'trend': trend,
            'sma20': latest_sma20,
            'sma50': latest_sma50,
            'sma200': latest_sma200
        }
    
    def _generate_volume_signals(self, data: pd.DataFrame) -> Dict:
        """Generate Volume-based signals"""
        latest_volume = data['Volume'].iloc[-1]
        latest_close = data['Close'].iloc[-1]
        latest_obv = data['OBV'].iloc[-1]
        
        if pd.isna(latest_volume) or pd.isna(latest_obv):
            return {'signal': 'neutral', 'strength': 0, 'reason': 'Insufficient data'}
        
        # Calculate average volume
        avg_volume = data['Volume'].tail(20).mean()
        
        # Volume spike
        volume_ratio = latest_volume / avg_volume
        
        if volume_ratio > 2.0:  # Volume spike
            if latest_close > data['Close'].iloc[-2]:  # Price up
                signal = 'buy'
                strength = min(volume_ratio / 5, 1.0)
                reason = f'High volume price increase (volume ratio: {volume_ratio:.2f})'
            else:  # Price down
                signal = 'sell'
                strength = min(volume_ratio / 5, 1.0)
                reason = f'High volume price decrease (volume ratio: {volume_ratio:.2f})'
        else:
            signal = 'hold'
            strength = 0.5
            reason = f'Normal volume (ratio: {volume_ratio:.2f})'
        
        return {
            'signal': signal,
            'strength': strength,
            'reason': reason,
            'volume_ratio': volume_ratio,
            'obv': latest_obv
        }
    
    def _generate_combined_signal(self, individual_signals: Dict) -> Dict:
        """Generate a combined signal from all individual signals"""
        if not individual_signals:
            return {'signal': 'neutral', 'strength': 0, 'reason': 'No signals available'}
        
        # Weight the signals
        signal_weights = {
            'RSI': 0.2,
            'MACD': 0.25,
            'Bollinger_Bands': 0.2,
            'Moving_Averages': 0.25,
            'Volume': 0.1
        }
        
        total_weight = 0
        weighted_score = 0
        
        for signal_name, signal_data in individual_signals.items():
            if signal_name == 'Combined':
                continue
                
            if signal_name in signal_weights and 'signal' in signal_data:
                weight = signal_weights[signal_name]
                total_weight += weight
                
                # Convert signal to numeric score
                if signal_data['signal'] == 'buy':
                    score = signal_data.get('strength', 0.5)
                elif signal_data['signal'] == 'sell':
                    score = -signal_data.get('strength', 0.5)
                else:
                    score = 0
                
                weighted_score += score * weight
        
        if total_weight == 0:
            return {'signal': 'neutral', 'strength': 0, 'reason': 'No weighted signals available'}
        
        # Normalize score
        normalized_score = weighted_score / total_weight
        
        # Determine final signal
        if normalized_score > 0.3:
            signal = 'buy'
            strength = min(normalized_score, 1.0)
            reason = 'Multiple indicators suggest bullish momentum'
        elif normalized_score < -0.3:
            signal = 'sell'
            strength = min(abs(normalized_score), 1.0)
            reason = 'Multiple indicators suggest bearish momentum'
        else:
            signal = 'hold'
            strength = 0.5
            reason = 'Mixed signals, maintaining current position'
        
        return {
            'signal': signal,
            'strength': strength,
            'reason': reason,
            'score': normalized_score,
            'individual_signals': individual_signals
        }


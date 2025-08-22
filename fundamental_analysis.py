import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging
from config import Config

logger = logging.getLogger(__name__)

class FundamentalAnalyzer:
    """Comprehensive fundamental analysis for stocks"""
    
    def __init__(self):
        self.min_market_cap = Config.MIN_MARKET_CAP
        self.max_pe_ratio = Config.MAX_PE_RATIO
        self.min_volume = Config.MIN_VOLUME
    
    def calculate_fundamental_score(self, fundamental_data: Dict) -> Dict:
        """Calculate comprehensive fundamental score for a stock"""
        if not fundamental_data:
            return {}
        
        try:
            scores = {}
            
            # Valuation score
            scores['valuation'] = self._calculate_valuation_score(fundamental_data)
            
            # Profitability score
            scores['profitability'] = self._calculate_profitability_score(fundamental_data)
            
            # Growth score
            scores['growth'] = self._calculate_growth_score(fundamental_data)
            
            # Financial health score
            scores['financial_health'] = self._calculate_financial_health_score(fundamental_data)
            
            # Overall score (weighted average)
            overall_score = self._calculate_overall_score(scores)
            scores['overall'] = overall_score
            
            # Add all metrics
            scores['metrics'] = fundamental_data
            
            return scores
            
        except Exception as e:
            logger.error(f"Error calculating fundamental score: {str(e)}")
            return {}
    
    def _calculate_valuation_score(self, data: Dict) -> float:
        """Calculate valuation score based on P/E, P/B, P/S ratios"""
        score = 0
        max_score = 100
        
        try:
            # P/E Ratio (lower is better, but not too low)
            pe_ratio = data.get('pe_ratio', 0)
            if pe_ratio > 0:
                if pe_ratio < 15:
                    score += 30  # Excellent value
                elif pe_ratio < 25:
                    score += 20  # Good value
                elif pe_ratio < 35:
                    score += 10  # Fair value
                else:
                    score += 0   # Overvalued
            
            # P/B Ratio (lower is better)
            pb_ratio = data.get('pb_ratio', 0)
            if pb_ratio > 0:
                if pb_ratio < 1:
                    score += 25  # Excellent value
                elif pb_ratio < 2:
                    score += 20  # Good value
                elif pb_ratio < 3:
                    score += 10  # Fair value
                else:
                    score += 0   # Overvalued
            
            # P/S Ratio (lower is better)
            price_to_sales = data.get('price_to_sales', 0)
            if price_to_sales > 0:
                if price_to_sales < 1:
                    score += 25  # Excellent value
                elif price_to_sales < 2:
                    score += 20  # Good value
                elif price_to_sales < 3:
                    score += 10  # Fair value
                else:
                    score += 0   # Overvalued
            
            # PEG Ratio (closer to 1 is better)
            peg_ratio = data.get('peg_ratio', 0)
            if peg_ratio > 0:
                if 0.8 <= peg_ratio <= 1.2:
                    score += 20  # Excellent value
                elif 0.5 <= peg_ratio <= 2.0:
                    score += 15  # Good value
                else:
                    score += 5   # Fair value
            
        except Exception as e:
            logger.error(f"Error calculating valuation score: {str(e)}")
        
        return min(score, max_score)
    
    def _calculate_profitability_score(self, data: Dict) -> float:
        """Calculate profitability score based on margins and returns"""
        score = 0
        max_score = 100
        
        try:
            # Return on Equity (higher is better)
            roe = data.get('roe', 0)
            if roe > 0:
                if roe > 0.20:
                    score += 25  # Excellent
                elif roe > 0.15:
                    score += 20  # Good
                elif roe > 0.10:
                    score += 15  # Fair
                elif roe > 0.05:
                    score += 10  # Poor
                else:
                    score += 0   # Very poor
            
            # Return on Assets (higher is better)
            roa = data.get('roa', 0)
            if roa > 0:
                if roa > 0.15:
                    score += 20  # Excellent
                elif roa > 0.10:
                    score += 15  # Good
                elif roa > 0.05:
                    score += 10  # Fair
                else:
                    score += 5   # Poor
            
            # Gross Margin (higher is better)
            gross_margin = data.get('gross_margin', 0)
            if gross_margin > 0:
                if gross_margin > 0.40:
                    score += 20  # Excellent
                elif gross_margin > 0.30:
                    score += 15  # Good
                elif gross_margin > 0.20:
                    score += 10  # Fair
                else:
                    score += 5   # Poor
            
            # Operating Margin (higher is better)
            operating_margin = data.get('operating_margin', 0)
            if operating_margin > 0:
                if operating_margin > 0.20:
                    score += 20  # Excellent
                elif operating_margin > 0.15:
                    score += 15  # Good
                elif operating_margin > 0.10:
                    score += 10  # Fair
                else:
                    score += 5   # Poor
            
            # Net Margin (higher is better)
            net_margin = data.get('net_margin', 0)
            if net_margin > 0:
                if net_margin > 0.15:
                    score += 15  # Excellent
                elif net_margin > 0.10:
                    score += 10  # Good
                elif net_margin > 0.05:
                    score += 5   # Fair
                else:
                    score += 0   # Poor
            
        except Exception as e:
            logger.error(f"Error calculating profitability score: {str(e)}")
        
        return min(score, max_score)
    
    def _calculate_growth_score(self, data: Dict) -> float:
        """Calculate growth score based on revenue and earnings growth"""
        score = 0
        max_score = 100
        
        try:
            # Revenue Growth (higher is better)
            revenue_growth = data.get('revenue_growth', 0)
            if revenue_growth > 0:
                if revenue_growth > 0.20:
                    score += 30  # Excellent
                elif revenue_growth > 0.15:
                    score += 25  # Good
                elif revenue_growth > 0.10:
                    score += 20  # Fair
                elif revenue_growth > 0.05:
                    score += 15  # Poor
                else:
                    score += 10  # Very poor
            
            # Earnings Growth (higher is better)
            earnings_growth = data.get('earnings_growth', 0)
            if earnings_growth > 0:
                if earnings_growth > 0.25:
                    score += 35  # Excellent
                elif earnings_growth > 0.20:
                    score += 30  # Good
                elif earnings_growth > 0.15:
                    score += 25  # Fair
                elif earnings_growth > 0.10:
                    score += 20  # Poor
                else:
                    score += 15  # Very poor
            
            # Book Value Growth
            book_value = data.get('book_value', 0)
            if book_value > 0:
                # This would need historical data for proper calculation
                score += 20  # Placeholder
            
            # Cash Flow Growth
            cash_per_share = data.get('cash_per_share', 0)
            if cash_per_share > 0:
                # This would need historical data for proper calculation
                score += 15  # Placeholder
            
        except Exception as e:
            logger.error(f"Error calculating growth score: {str(e)}")
        
        return min(score, max_score)
    
    def _calculate_financial_health_score(self, data: Dict) -> float:
        """Calculate financial health score based on debt and liquidity"""
        score = 0
        max_score = 100
        
        try:
            # Debt to Equity (lower is better)
            debt_to_equity = data.get('debt_to_equity', 0)
            if debt_to_equity > 0:
                if debt_to_equity < 0.3:
                    score += 25  # Excellent
                elif debt_to_equity < 0.5:
                    score += 20  # Good
                elif debt_to_equity < 0.7:
                    score += 15  # Fair
                elif debt_to_equity < 1.0:
                    score += 10  # Poor
                else:
                    score += 0   # Very poor
            
            # Current Ratio (higher is better, but not too high)
            current_ratio = data.get('current_ratio', 0)
            if current_ratio > 0:
                if 1.5 <= current_ratio <= 3.0:
                    score += 25  # Excellent
                elif 1.2 <= current_ratio <= 4.0:
                    score += 20  # Good
                elif 1.0 <= current_ratio <= 5.0:
                    score += 15  # Fair
                else:
                    score += 5   # Poor
            
            # Quick Ratio (higher is better)
            quick_ratio = data.get('quick_ratio', 0)
            if quick_ratio > 0:
                if quick_ratio > 1.0:
                    score += 20  # Excellent
                elif quick_ratio > 0.8:
                    score += 15  # Good
                elif quick_ratio > 0.6:
                    score += 10  # Fair
                else:
                    score += 5   # Poor
            
            # Interest Coverage (higher is better)
            # This would need EBIT and interest expense data
            score += 15  # Placeholder
            
            # Cash Position
            cash_per_share = data.get('cash_per_share', 0)
            if cash_per_share > 0:
                score += 15  # Good cash position
            
        except Exception as e:
            logger.error(f"Error calculating financial health score: {str(e)}")
        
        return min(score, max_score)
    
    def _calculate_overall_score(self, scores: Dict) -> float:
        """Calculate overall fundamental score as weighted average"""
        try:
            weights = {
                'valuation': 0.25,
                'profitability': 0.25,
                'growth': 0.25,
                'financial_health': 0.25
            }
            
            total_score = 0
            total_weight = 0
            
            for category, weight in weights.items():
                if category in scores and isinstance(scores[category], (int, float)):
                    total_score += scores[category] * weight
                    total_weight += weight
            
            if total_weight == 0:
                return 0
            
            return total_score / total_weight
            
        except Exception as e:
            logger.error(f"Error calculating overall score: {str(e)}")
            return 0
    
    def generate_fundamental_signals(self, fundamental_data: Dict) -> Dict:
        """Generate buy/sell signals based on fundamental analysis"""
        if not fundamental_data:
            return {}
        
        try:
            # Calculate scores
            scores = self.calculate_fundamental_score(fundamental_data)
            
            if not scores:
                return {}
            
            overall_score = scores.get('overall', 0)
            
            # Generate signal based on overall score
            if overall_score >= 80:
                signal = 'buy'
                strength = 0.9
                reason = f'Excellent fundamental score: {overall_score:.1f}/100'
            elif overall_score >= 70:
                signal = 'buy'
                strength = 0.7
                reason = f'Good fundamental score: {overall_score:.1f}/100'
            elif overall_score >= 60:
                signal = 'hold'
                strength = 0.6
                reason = f'Fair fundamental score: {overall_score:.1f}/100'
            elif overall_score >= 50:
                signal = 'hold'
                strength = 0.5
                reason = f'Below average fundamental score: {overall_score:.1f}/100'
            else:
                signal = 'sell'
                strength = 0.7
                reason = f'Poor fundamental score: {overall_score:.1f}/100'
            
            return {
                'signal': signal,
                'strength': strength,
                'reason': reason,
                'overall_score': overall_score,
                'category_scores': {
                    'valuation': scores.get('valuation', 0),
                    'profitability': scores.get('profitability', 0),
                    'growth': scores.get('growth', 0),
                    'financial_health': scores.get('financial_health', 0)
                },
                'metrics': fundamental_data
            }
            
        except Exception as e:
            logger.error(f"Error generating fundamental signals: {str(e)}")
            return {}
    
    def calculate_valuation_metrics(self, fundamental_data: Dict) -> Dict:
        """Calculate additional valuation metrics"""
        if not fundamental_data:
            return {}
        
        try:
            metrics = {}
            
            # Discounted Cash Flow (DCF) - Simplified
            if 'earnings_per_share' in fundamental_data and 'pe_ratio' in fundamental_data:
                eps = fundamental_data.get('earnings_per_share', 0)
                pe = fundamental_data.get('pe_ratio', 0)
                
                if eps > 0 and pe > 0:
                    # Simple DCF calculation
                    growth_rate = fundamental_data.get('earnings_growth', 0.05)  # Default 5%
                    discount_rate = 0.10  # 10% discount rate
                    
                    # Calculate present value of future earnings
                    future_eps = eps * (1 + growth_rate) ** 5
                    present_value = future_eps / (1 + discount_rate) ** 5
                    
                    metrics['dcf_value'] = present_value
                    metrics['dcf_premium'] = (present_value - eps) / eps if eps > 0 else 0
            
            # Dividend Discount Model (DDM)
            if 'dividend_yield' in fundamental_data and 'earnings_per_share' in fundamental_data:
                dividend_yield = fundamental_data.get('dividend_yield', 0)
                eps = fundamental_data.get('earnings_per_share', 0)
                
                if dividend_yield > 0 and eps > 0:
                    # Assume payout ratio and growth
                    payout_ratio = dividend_yield * pe if pe > 0 else 0.3
                    growth_rate = fundamental_data.get('earnings_growth', 0.05)
                    
                    if growth_rate < 0.10:  # Only if growth is reasonable
                        ddm_value = eps * payout_ratio / (0.10 - growth_rate)
                        metrics['ddm_value'] = ddm_value
                        metrics['ddm_premium'] = (ddm_value - eps) / eps if eps > 0 else 0
            
            # Enterprise Value metrics
            if 'enterprise_value' in fundamental_data and 'market_cap' in fundamental_data:
                ev = fundamental_data.get('enterprise_value', 0)
                market_cap = fundamental_data.get('market_cap', 0)
                
                if ev > 0 and market_cap > 0:
                    metrics['ev_to_market_cap'] = ev / market_cap
                    
                    # EV/EBITDA if available
                    if 'enterprise_to_ebitda' in fundamental_data:
                        metrics['ev_to_ebitda'] = fundamental_data.get('enterprise_to_ebitda', 0)
            
            # Return metrics
            if 'market_cap' in fundamental_data and 'book_value' in fundamental_data:
                book_value = fundamental_data.get('book_value', 0)
                shares = fundamental_data.get('shares_outstanding', 0)
                
                if book_value > 0 and shares > 0:
                    total_book_value = book_value * shares
                    market_cap = fundamental_data.get('market_cap', 0)
                    
                    if market_cap > 0:
                        metrics['price_to_book'] = market_cap / total_book_value
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating valuation metrics: {str(e)}")
            return {}
    
    def compare_with_peers(self, stock_data: Dict, peer_data: List[Dict]) -> Dict:
        """Compare stock fundamentals with peer companies"""
        if not stock_data or not peer_data:
            return {}
        
        try:
            comparison = {
                'stock_symbol': stock_data.get('symbol', ''),
                'peer_comparison': {},
                'rankings': {}
            }
            
            # Calculate peer averages
            peer_metrics = {}
            for peer in peer_data:
                for key, value in peer.items():
                    if key not in ['symbol', 'company_name'] and isinstance(value, (int, float)):
                        if key not in peer_metrics:
                            peer_metrics[key] = []
                        peer_metrics[key].append(value)
            
            # Calculate averages and compare
            for metric, values in peer_metrics.items():
                if values:
                    avg_value = np.mean(values)
                    stock_value = stock_data.get(metric, 0)
                    
                    if isinstance(stock_value, (int, float)) and avg_value != 0:
                        comparison['peer_comparison'][metric] = {
                            'stock_value': stock_value,
                            'peer_average': avg_value,
                            'difference': stock_value - avg_value,
                            'percent_difference': ((stock_value - avg_value) / avg_value) * 100
                        }
            
            # Calculate rankings
            for metric, values in peer_metrics.items():
                if values:
                    stock_value = stock_data.get(metric, 0)
                    if isinstance(stock_value, (int, float)):
                        # Sort values (lower is better for some metrics)
                        sorted_values = sorted(values)
                        if metric in ['pe_ratio', 'pb_ratio', 'debt_to_equity']:
                            # Lower is better
                            rank = sorted_values.index(stock_value) + 1
                        else:
                            # Higher is better
                            rank = len(sorted_values) - sorted_values.index(stock_value)
                        
                        comparison['rankings'][metric] = {
                            'rank': rank,
                            'total_peers': len(sorted_values),
                            'percentile': (rank / len(sorted_values)) * 100
                        }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing with peers: {str(e)}")
            return {}
    
    def generate_fundamental_report(self, fundamental_data: Dict, scores: Dict) -> Dict:
        """Generate comprehensive fundamental analysis report"""
        if not fundamental_data or not scores:
            return {}
        
        try:
            report = {
                'summary': {
                    'overall_score': scores.get('overall', 0),
                    'recommendation': self._get_recommendation(scores.get('overall', 0)),
                    'strengths': [],
                    'weaknesses': [],
                    'risks': [],
                    'opportunities': []
                },
                'detailed_analysis': {
                    'valuation': self._analyze_valuation(fundamental_data, scores),
                    'profitability': self._analyze_profitability(fundamental_data, scores),
                    'growth': self._analyze_growth(fundamental_data, scores),
                    'financial_health': self._analyze_financial_health(fundamental_data, scores)
                },
                'key_metrics': fundamental_data,
                'scores': scores
            }
            
            # Identify strengths and weaknesses
            report['summary']['strengths'] = self._identify_strengths(scores)
            report['summary']['weaknesses'] = self._identify_weaknesses(scores)
            report['summary']['risks'] = self._identify_risks(fundamental_data)
            report['summary']['opportunities'] = self._identify_opportunities(fundamental_data)
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating fundamental report: {str(e)}")
            return {}
    
    def _get_recommendation(self, overall_score: float) -> str:
        """Get recommendation based on overall score"""
        if overall_score >= 80:
            return "Strong Buy"
        elif overall_score >= 70:
            return "Buy"
        elif overall_score >= 60:
            return "Hold"
        elif overall_score >= 50:
            return "Weak Hold"
        else:
            return "Sell"
    
    def _analyze_valuation(self, data: Dict, scores: Dict) -> Dict:
        """Analyze valuation metrics"""
        valuation_score = scores.get('valuation', 0)
        
        analysis = {
            'score': valuation_score,
            'grade': self._get_grade(valuation_score),
            'insights': []
        }
        
        # Add specific insights
        pe_ratio = data.get('pe_ratio', 0)
        if pe_ratio > 0:
            if pe_ratio < 15:
                analysis['insights'].append("P/E ratio indicates excellent value")
            elif pe_ratio > 30:
                analysis['insights'].append("P/E ratio suggests overvaluation")
        
        pb_ratio = data.get('pb_ratio', 0)
        if pb_ratio > 0:
            if pb_ratio < 1:
                analysis['insights'].append("P/B ratio indicates strong asset value")
            elif pb_ratio > 3:
                analysis['insights'].append("P/B ratio suggests premium pricing")
        
        return analysis
    
    def _analyze_profitability(self, data: Dict, scores: Dict) -> Dict:
        """Analyze profitability metrics"""
        profitability_score = scores.get('profitability', 0)
        
        analysis = {
            'score': profitability_score,
            'grade': self._get_grade(profitability_score),
            'insights': []
        }
        
        # Add specific insights
        roe = data.get('roe', 0)
        if roe > 0.20:
            analysis['insights'].append("Excellent return on equity")
        elif roe < 0.05:
            analysis['insights'].append("Poor return on equity")
        
        gross_margin = data.get('gross_margin', 0)
        if gross_margin > 0.40:
            analysis['insights'].append("Strong gross margins")
        elif gross_margin < 0.20:
            analysis['insights'].append("Weak gross margins")
        
        return analysis
    
    def _analyze_growth(self, data: Dict, scores: Dict) -> Dict:
        """Analyze growth metrics"""
        growth_score = scores.get('growth', 0)
        
        analysis = {
            'score': growth_score,
            'grade': self._get_grade(growth_score),
            'insights': []
        }
        
        # Add specific insights
        revenue_growth = data.get('revenue_growth', 0)
        if revenue_growth > 0.20:
            analysis['insights'].append("Strong revenue growth")
        elif revenue_growth < 0.05:
            analysis['insights'].append("Weak revenue growth")
        
        earnings_growth = data.get('earnings_growth', 0)
        if earnings_growth > 0.25:
            analysis['insights'].append("Excellent earnings growth")
        elif earnings_growth < 0.10:
            analysis['insights'].append("Poor earnings growth")
        
        return analysis
    
    def _analyze_financial_health(self, data: Dict, scores: Dict) -> Dict:
        """Analyze financial health metrics"""
        financial_health_score = scores.get('financial_health', 0)
        
        analysis = {
            'score': financial_health_score,
            'grade': self._get_grade(financial_health_score),
            'insights': []
        }
        
        # Add specific insights
        debt_to_equity = data.get('debt_to_equity', 0)
        if debt_to_equity < 0.3:
            analysis['insights'].append("Low debt levels")
        elif debt_to_equity > 1.0:
            analysis['insights'].append("High debt levels")
        
        current_ratio = data.get('current_ratio', 0)
        if current_ratio > 2.0:
            analysis['insights'].append("Strong liquidity position")
        elif current_ratio < 1.0:
            analysis['insights'].append("Weak liquidity position")
        
        return analysis
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B+"
        elif score >= 60:
            return "B"
        elif score >= 50:
            return "C+"
        elif score >= 40:
            return "C"
        elif score >= 30:
            return "D"
        else:
            return "F"
    
    def _identify_strengths(self, scores: Dict) -> List[str]:
        """Identify company strengths"""
        strengths = []
        
        if scores.get('valuation', 0) >= 70:
            strengths.append("Strong valuation metrics")
        if scores.get('profitability', 0) >= 70:
            strengths.append("High profitability")
        if scores.get('growth', 0) >= 70:
            strengths.append("Strong growth trajectory")
        if scores.get('financial_health', 0) >= 70:
            strengths.append("Solid financial health")
        
        return strengths
    
    def _identify_weaknesses(self, scores: Dict) -> List[str]:
        """Identify company weaknesses"""
        weaknesses = []
        
        if scores.get('valuation', 0) < 50:
            weaknesses.append("Poor valuation metrics")
        if scores.get('profitability', 0) < 50:
            weaknesses.append("Low profitability")
        if scores.get('growth', 0) < 50:
            weaknesses.append("Weak growth")
        if scores.get('financial_health', 0) < 50:
            weaknesses.append("Poor financial health")
        
        return weaknesses
    
    def _identify_risks(self, data: Dict) -> List[str]:
        """Identify potential risks"""
        risks = []
        
        debt_to_equity = data.get('debt_to_equity', 0)
        if debt_to_equity > 1.0:
            risks.append("High debt levels")
        
        pe_ratio = data.get('pe_ratio', 0)
        if pe_ratio > 30:
            risks.append("High valuation multiples")
        
        beta = data.get('beta', 0)
        if beta > 1.5:
            risks.append("High market volatility")
        
        return risks
    
    def _identify_opportunities(self, data: Dict) -> List[str]:
        """Identify potential opportunities"""
        opportunities = []
        
        pe_ratio = data.get('pe_ratio', 0)
        if pe_ratio < 15:
            opportunities.append("Undervalued based on P/E ratio")
        
        revenue_growth = data.get('revenue_growth', 0)
        if revenue_growth > 0.15:
            opportunities.append("Strong revenue growth potential")
        
        market_cap = data.get('market_cap', 0)
        if market_cap < 10000000000:  # $10B
            opportunities.append("Mid-cap growth potential")
        
        return opportunities

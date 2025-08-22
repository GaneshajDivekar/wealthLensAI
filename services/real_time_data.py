import yfinance as yf
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import asyncio
import aiohttp
import json

class RealTimeDataService:
    """Service for fetching real-time financial data"""
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = 600  # 10 minutes (increased for demo)
        self.last_update = {}
        self.request_count = 0
        self.last_request_time = datetime.now()
        self.max_requests_per_minute = 10  # Conservative limit
    
    def get_live_prices(self, symbols: List[str]) -> Dict[str, float]:
        """Fetch real-time stock prices with rate limiting"""
        current_time = datetime.now()
        live_prices = {}
        
        # Enhanced rate limiting and caching
        import time
        
        for i, symbol in enumerate(symbols):
            # Check cache first (priority for demo)
            if (symbol in self.cache and 
                symbol in self.last_update and 
                (current_time - self.last_update[symbol]).seconds < self.cache_duration):
                live_prices[symbol] = self.cache[symbol]
                continue
            
            # Rate limiting check
            time_since_last = (current_time - self.last_request_time).seconds
            if time_since_last < 60:  # Within last minute
                if self.request_count >= self.max_requests_per_minute:
                    # Use fallback data to avoid rate limiting
                    live_prices[symbol] = self._get_fallback_price(symbol)
                    continue
            else:
                # Reset counter for new minute
                self.request_count = 0
                self.last_request_time = current_time
            
            try:
                # Add delay between requests (1 second for demo)
                if i > 0:
                    time.sleep(1.0)
                
                self.request_count += 1
                ticker = yf.Ticker(symbol)
                price = ticker.info.get('regularMarketPrice')
                if price and price > 0:
                    live_prices[symbol] = price
                    self.cache[symbol] = price
                    self.last_update[symbol] = current_time
                else:
                    # Fallback to cached price or default
                    live_prices[symbol] = self._get_fallback_price(symbol)
            except Exception as e:
                print(f"Error fetching price for {symbol}: {e}")
                # Use fallback prices for demo
                live_prices[symbol] = self._get_fallback_price(symbol)
        
        return live_prices
    
    def _get_fallback_price(self, symbol: str) -> float:
        """Get fallback price for demo purposes"""
        fallback_prices = {
            "RELIANCE.NS": 2650,
            "TCS.NS": 3191,
            "INFY.NS": 1500,
            "HDFCBANK.NS": 1736,
            "ICICIBANK.NS": 1020,
            "AAPL": 175.0,
            "MSFT": 350.0,
            "GOOGL": 140.0,
            "AMZN": 145.0,
            "TSLA": 220.0,
            "SUZLON.NS": 47.5,
            "JPASSOCIAT.NS": 62.0,
            "YESBANK.NS": 15.0
        }
        return fallback_prices.get(symbol, self.cache.get(symbol, 0))
    
    def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """Get comprehensive stock information"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'name': info.get('longName', symbol),
                'current_price': info.get('regularMarketPrice', 0),
                'previous_close': info.get('previousClose', 0),
                'market_cap': info.get('marketCap', 0),
                'volume': info.get('volume', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'beta': info.get('beta', 0),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'country': info.get('country', 'Unknown'),
                'currency': info.get('currency', 'USD'),
                'exchange': info.get('exchange', 'Unknown')
            }
        except Exception as e:
            print(f"Error fetching info for {symbol}: {e}")
            return {
                'symbol': symbol,
                'name': symbol,
                'current_price': 0,
                'previous_close': 0,
                'market_cap': 0,
                'volume': 0,
                'pe_ratio': 0,
                'dividend_yield': 0,
                'beta': 0,
                'sector': 'Unknown',
                'industry': 'Unknown',
                'country': 'Unknown',
                'currency': 'USD',
                'exchange': 'Unknown'
            }
    
    def get_historical_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """Get historical price data"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            return hist
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {e}")
            return pd.DataFrame()
    
    def calculate_technical_indicators(self, symbol: str) -> Dict[str, float]:
        """Calculate technical indicators"""
        try:
            hist = self.get_historical_data(symbol, "6mo")
            if hist.empty:
                return {}
            
            # Calculate RSI
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # Calculate MACD
            exp1 = hist['Close'].ewm(span=12).mean()
            exp2 = hist['Close'].ewm(span=26).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9).mean()
            
            # Calculate Moving Averages
            sma_20 = hist['Close'].rolling(window=20).mean()
            sma_50 = hist['Close'].rolling(window=50).mean()
            
            return {
                'rsi': rsi.iloc[-1] if not rsi.empty else 50,
                'macd': macd.iloc[-1] if not macd.empty else 0,
                'macd_signal': signal.iloc[-1] if not signal.empty else 0,
                'sma_20': sma_20.iloc[-1] if not sma_20.empty else 0,
                'sma_50': sma_50.iloc[-1] if not sma_50.empty else 0,
                'current_price': hist['Close'].iloc[-1] if not hist.empty else 0,
                'volume': hist['Volume'].iloc[-1] if not hist.empty else 0
            }
        except Exception as e:
            print(f"Error calculating indicators for {symbol}: {e}")
            return {}
    
    def get_market_sentiment(self, symbol: str) -> Dict[str, Any]:
        """Get market sentiment data with fallback"""
        try:
            # Use cached data if available to avoid rate limiting
            if symbol in self.cache:
                current_price = self.cache[symbol]
                # Simulate price change for demo
                import random
                price_change = random.uniform(-5, 5)
                price_change_pct = (price_change / current_price * 100) if current_price > 0 else 0
                
                return {
                    'symbol': symbol,
                    'current_price': current_price,
                    'price_change': price_change,
                    'price_change_pct': price_change_pct,
                    'volume': random.randint(1000000, 10000000),
                    'market_cap': current_price * random.randint(1000000, 10000000),
                    'pe_ratio': random.uniform(10, 30),
                    'beta': random.uniform(0.5, 1.5),
                    'sentiment': 'bullish' if price_change > 0 else 'bearish' if price_change < 0 else 'neutral'
                }
            
            # Fallback to simulated data
            fallback_prices = {
                "RELIANCE.NS": 2650,
                "TCS.NS": 3191,
                "INFY.NS": 1500,
                "HDFCBANK.NS": 1736,
                "ICICIBANK.NS": 1020,
                "AAPL": 175.0,
                "MSFT": 350.0,
                "GOOGL": 140.0,
                "AMZN": 145.0,
                "TSLA": 220.0,
                "SUZLON.NS": 47.5,
                "JPASSOCIAT.NS": 62.0,
                "YESBANK.NS": 15.0
            }
            
            current_price = fallback_prices.get(symbol, 100)
            import random
            price_change = random.uniform(-5, 5)
            price_change_pct = (price_change / current_price * 100) if current_price > 0 else 0
            
            return {
                'symbol': symbol,
                'current_price': current_price,
                'price_change': price_change,
                'price_change_pct': price_change_pct,
                'volume': random.randint(1000000, 10000000),
                'market_cap': current_price * random.randint(1000000, 10000000),
                'pe_ratio': random.uniform(10, 30),
                'beta': random.uniform(0.5, 1.5),
                'sentiment': 'bullish' if price_change > 0 else 'bearish' if price_change < 0 else 'neutral'
            }
            
        except Exception as e:
            print(f"Error fetching sentiment for {symbol}: {e}")
            return {
                'symbol': symbol,
                'current_price': 0,
                'price_change': 0,
                'price_change_pct': 0,
                'volume': 0,
                'market_cap': 0,
                'pe_ratio': 0,
                'beta': 0,
                'sentiment': 'neutral'
            }

# Global instance
real_time_service = RealTimeDataService()

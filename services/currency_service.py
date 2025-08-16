import requests
import json
from typing import Dict, Optional
from datetime import datetime, timedelta

class CurrencyService:
    """Service for currency conversion and exchange rates"""
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = 3600  # 1 hour
        self.last_update = {}
        self.base_url = "https://api.exchangerate-api.com/v4/latest"
    
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """Get exchange rate between two currencies"""
        current_time = datetime.now()
        cache_key = f"{from_currency}_{to_currency}"
        
        # Check cache first
        if (cache_key in self.cache and 
            cache_key in self.last_update and 
            (current_time - self.last_update[cache_key]).seconds < self.cache_duration):
            return self.cache[cache_key]
        
        try:
            # Use free exchange rate API
            url = f"{self.base_url}/{from_currency}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                rates = data.get('rates', {})
                rate = rates.get(to_currency, 1.0)
                
                # Cache the result
                self.cache[cache_key] = rate
                self.last_update[cache_key] = current_time
                
                return rate
            else:
                # Fallback to cached rate or default
                return self.cache.get(cache_key, 1.0)
                
        except Exception as e:
            print(f"Error fetching exchange rate: {e}")
            # Fallback rates (approximate)
            fallback_rates = {
                "INR_USD": 0.012,  # 1 INR = 0.012 USD
                "USD_INR": 83.0,   # 1 USD = 83 INR
                "EUR_USD": 1.08,   # 1 EUR = 1.08 USD
                "USD_EUR": 0.93,   # 1 USD = 0.93 EUR
            }
            return fallback_rates.get(cache_key, 1.0)
    
    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Convert amount from one currency to another"""
        if from_currency == to_currency:
            return amount
        
        rate = self.get_exchange_rate(from_currency, to_currency)
        return amount * rate
    
    def format_currency(self, amount: float, currency: str) -> str:
        """Format currency amount with proper symbols"""
        currency_symbols = {
            "USD": "$",
            "INR": "₹",
            "EUR": "€",
            "GBP": "£"
        }
        
        symbol = currency_symbols.get(currency, currency)
        
        if currency == "INR":
            return f"{symbol}{amount:,.0f}"
        elif currency == "USD":
            return f"{symbol}{amount:,.2f}"
        else:
            return f"{symbol}{amount:,.2f}"
    
    def get_portfolio_in_usd(self, portfolio_data: Dict) -> Dict:
        """Convert portfolio values to USD"""
        try:
            # Get INR to USD rate
            inr_to_usd_rate = self.get_exchange_rate("INR", "USD")
            
            # Convert portfolio values
            total_value_inr = sum(stock.get('quantity', 0) * stock.get('current_price', 0) for stock in portfolio_data['stocks'])
            total_investment_inr = sum(stock.get('quantity', 0) * stock.get('avg_price', 0) for stock in portfolio_data['stocks'])
            
            total_value_usd = self.convert_currency(total_value_inr, "INR", "USD")
            total_investment_usd = self.convert_currency(total_investment_inr, "INR", "USD")
            total_pnl_usd = total_value_usd - total_investment_usd
            
            return {
                "total_value_inr": total_value_inr,
                "total_value_usd": total_value_usd,
                "total_investment_inr": total_investment_inr,
                "total_investment_usd": total_investment_usd,
                "total_pnl_inr": total_value_inr - total_investment_inr,
                "total_pnl_usd": total_pnl_usd,
                "exchange_rate": inr_to_usd_rate,
                "currency": "USD"
            }
        except Exception as e:
            print(f"Error converting portfolio to USD: {e}")
            return {}
    
    def get_stock_price_in_usd(self, stock_data: Dict) -> Dict:
        """Convert stock price to USD"""
        try:
            current_price_inr = stock_data.get('current_price', 0)
            current_price_usd = self.convert_currency(current_price_inr, "INR", "USD")
            
            return {
                "price_inr": current_price_inr,
                "price_usd": current_price_usd,
                "exchange_rate": self.get_exchange_rate("INR", "USD")
            }
        except Exception as e:
            print(f"Error converting stock price to USD: {e}")
            return {}

# Global instance
currency_service = CurrencyService()

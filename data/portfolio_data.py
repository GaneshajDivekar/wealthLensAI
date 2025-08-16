from typing import Dict, List
from datetime import datetime
from services.real_time_data import real_time_service

# Hardcoded Portfolio Data with Real-Time Price Updates
PORTFOLIO_DATA = {
    "stocks": [
        {
            "symbol": "RELIANCE.NS",
            "name": "Reliance Industries",
            "quantity": 1000,
            "avg_price": 2500,
            "current_price": 2650,
            "sector": "Oil & Gas",
            "country": "India",
            "market_cap": "Large Cap"
        },
        {
            "symbol": "TCS.NS",
            "name": "Tata Consultancy Services",
            "quantity": 500,
            "avg_price": 3800,
            "current_price": 3950,
            "sector": "IT",
            "country": "India",
            "market_cap": "Large Cap"
        },
        {
            "symbol": "INFY.NS",
            "name": "Infosys",
            "quantity": 800,
            "avg_price": 1400,
            "current_price": 1520,
            "sector": "IT",
            "country": "India",
            "market_cap": "Large Cap"
        },
        {
            "symbol": "HDFCBANK.NS",
            "name": "HDFC Bank",
            "quantity": 1200,
            "avg_price": 1600,
            "current_price": 1680,
            "sector": "Banking",
            "country": "India",
            "market_cap": "Large Cap"
        },
        {
            "symbol": "ICICIBANK.NS",
            "name": "ICICI Bank",
            "quantity": 1500,
            "avg_price": 900,
            "current_price": 950,
            "sector": "Banking",
            "country": "India",
            "market_cap": "Large Cap"
        },
        {
            "symbol": "AAPL",
            "name": "Apple Inc",
            "quantity": 50,
            "avg_price": 150,
            "current_price": 175,
            "sector": "Technology",
            "country": "USA",
            "market_cap": "Large Cap"
        },
        {
            "symbol": "MSFT",
            "name": "Microsoft Corporation",
            "quantity": 40,
            "avg_price": 280,
            "current_price": 320,
            "sector": "Technology",
            "country": "USA",
            "market_cap": "Large Cap"
        },
        {
            "symbol": "GOOGL",
            "name": "Alphabet Inc",
            "quantity": 30,
            "avg_price": 120,
            "current_price": 140,
            "sector": "Technology",
            "country": "USA",
            "market_cap": "Large Cap"
        },
        {
            "symbol": "AMZN",
            "name": "Amazon.com Inc",
            "quantity": 60,
            "avg_price": 130,
            "current_price": 145,
            "sector": "Consumer Discretionary",
            "country": "USA",
            "market_cap": "Large Cap"
        },
        {
            "symbol": "TSLA",
            "name": "Tesla Inc",
            "quantity": 100,
            "avg_price": 200,
            "current_price": 220,
            "sector": "Automotive",
            "country": "USA",
            "market_cap": "Large Cap"
        },
        # Penny Stocks (Low price stocks)
        {
            "symbol": "SUZLON.NS",
            "name": "Suzlon Energy",
            "quantity": 5000,
            "avg_price": 8,
            "current_price": 9.5,
            "sector": "Energy",
            "country": "India",
            "market_cap": "Small Cap"
        },
        {
            "symbol": "JPASSOCIAT.NS",
            "name": "Jaiprakash Associates",
            "quantity": 10000,
            "avg_price": 5,
            "current_price": 6.2,
            "sector": "Construction",
            "country": "India",
            "market_cap": "Small Cap"
        },
        {
            "symbol": "YESBANK.NS",
            "name": "Yes Bank",
            "quantity": 2000,
            "avg_price": 12,
            "current_price": 15.5,
            "sector": "Banking",
            "country": "India",
            "market_cap": "Mid Cap"
        }
    ],
    "mutual_funds": [
        {
            "name": "HDFC Mid-Cap Opportunities Fund",
            "quantity": 1000,
            "nav": 45.5,
            "current_nav": 48.2,
            "category": "Mid Cap"
        },
        {
            "name": "Axis Bluechip Fund",
            "quantity": 800,
            "nav": 35.2,
            "current_nav": 37.8,
            "category": "Large Cap"
        }
    ],
    "last_updated": datetime.now().isoformat()
}

# Sector-wise classification
SECTORS = {
    "Technology": ["TCS.NS", "INFY.NS", "AAPL", "MSFT", "GOOGL"],
    "Banking": ["HDFCBANK.NS", "ICICIBANK.NS", "YESBANK.NS"],
    "Oil & Gas": ["RELIANCE.NS"],
    "Consumer Discretionary": ["AMZN"],
    "Automotive": ["TSLA"],
    "Energy": ["SUZLON.NS"],
    "Construction": ["JPASSOCIAT.NS"]
}

# Country-wise classification
COUNTRIES = {
    "India": ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", 
              "SUZLON.NS", "JPASSOCIAT.NS", "YESBANK.NS"],
    "USA": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]
}

# Market cap classification
MARKET_CAPS = {
    "Large Cap": ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
                  "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
    "Mid Cap": ["YESBANK.NS"],
    "Small Cap": ["SUZLON.NS", "JPASSOCIAT.NS"]
}

def get_portfolio_summary():
    """Calculate portfolio summary"""
    total_value = 0
    total_investment = 0
    
    for stock in PORTFOLIO_DATA["stocks"]:
        current_value = stock["quantity"] * stock["current_price"]
        investment_value = stock["quantity"] * stock["avg_price"]
        total_value += current_value
        total_investment += investment_value
    
    for fund in PORTFOLIO_DATA["mutual_funds"]:
        current_value = fund["quantity"] * fund["current_nav"]
        investment_value = fund["quantity"] * fund["nav"]
        total_value += current_value
        total_investment += investment_value
    
    return {
        "total_value": total_value,
        "total_investment": total_investment,
        "total_pnl": total_value - total_investment,
        "total_pnl_percentage": ((total_value - total_investment) / total_investment) * 100 if total_investment > 0 else 0
    }

def get_stocks_by_criteria(criteria: str, value: str):
    """Get stocks filtered by criteria"""
    if criteria == "country":
        symbols = COUNTRIES.get(value, [])
    elif criteria == "sector":
        symbols = SECTORS.get(value, [])
    elif criteria == "market_cap":
        symbols = MARKET_CAPS.get(value, [])
    else:
        return []
    
    return [stock for stock in PORTFOLIO_DATA["stocks"] if stock["symbol"] in symbols]

def get_penny_stocks():
    """Get penny stocks (low price stocks)"""
    return [stock for stock in PORTFOLIO_DATA["stocks"] if stock["current_price"] < 20]

def get_portfolio_data():
    """Get complete portfolio data with real-time prices"""
    # Get all symbols from portfolio
    symbols = [stock["symbol"] for stock in PORTFOLIO_DATA["stocks"]]
    
    # Fetch real-time prices
    live_prices = real_time_service.get_live_prices(symbols)
    
    # Update portfolio with live prices
    updated_portfolio = PORTFOLIO_DATA.copy()
    for stock in updated_portfolio["stocks"]:
        symbol = stock["symbol"]
        if symbol in live_prices and live_prices[symbol] > 0:
            stock["current_price"] = live_prices[symbol]
            # Calculate current value and P&L
            stock["current_value"] = stock["quantity"] * stock["current_price"]
            stock["investment_amount"] = stock["quantity"] * stock["avg_price"]
            stock["pnl"] = stock["current_value"] - stock["investment_amount"]
            stock["pnl_percentage"] = (stock["pnl"] / stock["investment_amount"]) * 100 if stock["investment_amount"] > 0 else 0
    
    return updated_portfolio

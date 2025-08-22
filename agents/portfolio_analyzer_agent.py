from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from data.portfolio_data import PORTFOLIO_DATA, get_portfolio_summary, get_stocks_by_criteria, get_penny_stocks, get_portfolio_data
from services.chart_service import chart_service
from services.currency_service import currency_service
import yfinance as yf
import pandas as pd

class PortfolioAnalyzerAgent(BaseAgent):
    """Agent for analyzing portfolio performance and providing insights"""
    
    def __init__(self):
        super().__init__(
            name="Portfolio Analyzer",
            description="Analyzes portfolio performance, calculates returns, and provides investment insights"
        )
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process portfolio analysis request"""
        query = input_data.get("query", "").lower()
        user_language = input_data.get("language", "normal")
        
        # Analyze portfolio performance
        summary = get_portfolio_summary()
        
        if "portfolio summary" in query or "portfolio value" in query:
            return self._generate_portfolio_summary(summary, user_language)
        
        elif "penny stocks" in query or "low price stocks" in query:
            return self._analyze_penny_stocks(user_language)
        
        elif "sector analysis" in query or "sector breakdown" in query:
            return self._analyze_sectors(user_language)
        
        elif "country analysis" in query or "geographic breakdown" in query:
            return self._analyze_countries(user_language)
        
        elif "enlist stocks" in query or "list stocks" in query or "show stocks" in query:
            return self._enlist_stocks(user_language)
        
        elif "enlist sectors" in query or "list sectors" in query or "show sectors" in query:
            return self._enlist_sectors(user_language)
        
        elif "enlist countries" in query or "list countries" in query or "show countries" in query:
            return self._enlist_countries(user_language)
        
        elif "performance" in query or "returns" in query:
            return self._analyze_performance(summary, user_language)
        
        elif "risk" in query or "volatility" in query:
            return self._analyze_risk(user_language)
        
        else:
            return self._generate_comprehensive_analysis(summary, user_language)
    
    def _generate_portfolio_summary(self, summary: Dict, language: str) -> Dict[str, Any]:
        """Generate portfolio summary with charts"""
        # Get real-time portfolio data
        portfolio_data = get_portfolio_data()
        
        # Generate charts
        pie_chart = chart_service.generate_portfolio_pie_chart(portfolio_data)
        performance_chart = chart_service.generate_portfolio_performance_chart(portfolio_data)
        
        if language == "genz":
            response = f"""
            🔥 Your Portfolio Status 🔥
            
            💰 Total Value: ₹{summary['total_value']:,.0f}
            📈 Total Investment: ₹{summary['total_investment']:,.0f}
            🚀 P&L: ₹{summary['total_pnl']:,.0f} ({summary['total_pnl_percentage']:.2f}%)
            
            {self._get_emoji_status(summary['total_pnl_percentage'])}
            
            📊 Portfolio Distribution:
            {pie_chart}
            
            📈 Performance Analysis:
            {performance_chart}
            """
        else:
            response = f"""
            Portfolio Summary:
            
            Total Portfolio Value: ₹{summary['total_value']:,.0f}
            Total Investment: ₹{summary['total_investment']:,.0f}
            Total P&L: ₹{summary['total_pnl']:,.0f} ({summary['total_pnl_percentage']:.2f}%)
            
            {self._get_performance_status(summary['total_pnl_percentage'])}
            
            Portfolio Distribution:
            {pie_chart}
            
            Performance Analysis:
            {performance_chart}
            """
        
        return {
            "agent": self.name,
            "response": response + "\n\n📊 Source: Portfolio Analyzer Agent",
            "data": summary,
            "type": "portfolio_summary"
        }
    
    def _analyze_penny_stocks(self, language: str) -> Dict[str, Any]:
        """Analyze penny stocks"""
        penny_stocks = get_penny_stocks()
        
        if language == "genz":
            response = f"""
            🪙 Your Penny Stocks Collection 🪙
            
            Found {len(penny_stocks)} penny stocks in your portfolio:
            """
            for stock in penny_stocks:
                pnl = (stock['current_price'] - stock['avg_price']) * stock['quantity']
                pnl_pct = ((stock['current_price'] - stock['avg_price']) / stock['avg_price']) * 100
                response += f"""
                📊 {stock['name']} ({stock['symbol']})
                💵 Current: ₹{stock['current_price']} | Avg: ₹{stock['avg_price']}
                📈 P&L: ₹{pnl:,.0f} ({pnl_pct:.2f}%)
                """
        else:
            response = f"Found {len(penny_stocks)} penny stocks in your portfolio:\n"
            for stock in penny_stocks:
                pnl = (stock['current_price'] - stock['avg_price']) * stock['quantity']
                pnl_pct = ((stock['current_price'] - stock['avg_price']) / stock['avg_price']) * 100
                response += f"""
                {stock['name']} ({stock['symbol']})
                Current: ₹{stock['current_price']} | Avg: ₹{stock['avg_price']}
                P&L: ₹{pnl:,.0f} ({pnl_pct:.2f}%)
                """
        
        return {
            "agent": self.name,
            "response": response + "\n\n📊 Source: Portfolio Analyzer Agent",
            "data": penny_stocks,
            "type": "penny_stocks_analysis"
        }
    
    def _analyze_sectors(self, language: str) -> Dict[str, Any]:
        """Analyze sector breakdown"""
        sectors = {}
        for stock in PORTFOLIO_DATA["stocks"]:
            sector = stock["sector"]
            if sector not in sectors:
                sectors[sector] = {"stocks": [], "total_value": 0}
            sectors[sector]["stocks"].append(stock)
            sectors[sector]["total_value"] += stock["quantity"] * stock["current_price"]
        
        if language == "genz":
            response = "🏢 Sector Breakdown 🏢\n\n"
            for sector, data in sectors.items():
                response += f"📊 {sector}: ₹{data['total_value']:,.0f}\n"
        else:
            response = "Sector Breakdown:\n\n"
            for sector, data in sectors.items():
                response += f"{sector}: ₹{data['total_value']:,.0f}\n"
        
        return {
            "agent": self.name,
            "response": response + "\n\n📊 Source: Portfolio Analyzer Agent",
            "data": sectors,
            "type": "sector_analysis"
        }
    
    def _analyze_countries(self, language: str) -> Dict[str, Any]:
        """Analyze geographic breakdown"""
        countries = {}
        for stock in PORTFOLIO_DATA["stocks"]:
            country = stock["country"]
            if country not in countries:
                countries[country] = {"stocks": [], "total_value": 0}
            countries[country]["stocks"].append(stock)
            countries[country]["total_value"] += stock["quantity"] * stock["current_price"]
        
        if language == "genz":
            response = "🌍 Geographic Breakdown 🌍\n\n"
            for country, data in countries.items():
                response += f"🇮🇳 {country}: ₹{data['total_value']:,.0f}\n" if country == "India" else f"🇺🇸 {country}: ₹{data['total_value']:,.0f}\n"
        else:
            response = "Geographic Breakdown:\n\n"
            for country, data in countries.items():
                response += f"{country}: ₹{data['total_value']:,.0f}\n"
        
        return {
            "agent": self.name,
            "response": response + "\n\n📊 Source: Portfolio Analyzer Agent",
            "data": countries,
            "type": "country_analysis"
        }
    
    def _analyze_performance(self, summary: Dict, language: str) -> Dict[str, Any]:
        """Analyze portfolio performance"""
        if language == "genz":
            response = f"""
            📊 Performance Analysis 📊
            
            🎯 Overall Return: {summary['total_pnl_percentage']:.2f}%
            💰 Absolute Gain: ₹{summary['total_pnl']:,.0f}
            
            {self._get_performance_insight(summary['total_pnl_percentage'])}
            """
        else:
            response = f"""
            Performance Analysis:
            
            Overall Return: {summary['total_pnl_percentage']:.2f}%
            Absolute Gain: ₹{summary['total_pnl']:,.0f}
            
            {self._get_performance_insight(summary['total_pnl_percentage'])}
            """
        
        return {
            "agent": self.name,
            "response": response,
            "data": summary,
            "type": "performance_analysis"
        }
    
    def _analyze_risk(self, language: str) -> Dict[str, Any]:
        """Analyze portfolio risk"""
        # Simple risk analysis based on diversification
        total_stocks = len(PORTFOLIO_DATA["stocks"])
        sectors = len(set(stock["sector"] for stock in PORTFOLIO_DATA["stocks"]))
        countries = len(set(stock["country"] for stock in PORTFOLIO_DATA["stocks"]))
        
        if language == "genz":
            response = f"""
            ⚠️ Risk Analysis ⚠️
            
            📈 Diversification Score: {self._calculate_diversification_score(total_stocks, sectors, countries)}/10
            🏢 Sectors: {sectors}
            🌍 Countries: {countries}
            📊 Total Stocks: {total_stocks}
            
            {self._get_risk_insight(total_stocks, sectors, countries)}
            """
        else:
            response = f"""
            Risk Analysis:
            
            Diversification Score: {self._calculate_diversification_score(total_stocks, sectors, countries)}/10
            Sectors: {sectors}
            Countries: {countries}
            Total Stocks: {total_stocks}
            
            {self._get_risk_insight(total_stocks, sectors, countries)}
            """
        
        return {
            "agent": self.name,
            "response": response,
            "data": {"total_stocks": total_stocks, "sectors": sectors, "countries": countries},
            "type": "risk_analysis"
        }
    
    def _generate_comprehensive_analysis(self, summary: Dict, language: str) -> Dict[str, Any]:
        """Generate comprehensive portfolio analysis"""
        if language == "genz":
            response = f"""
            🚀 Complete Portfolio Analysis 🚀
            
            💰 Portfolio Value: ₹{summary['total_value']:,.0f}
            📈 Total Return: {summary['total_pnl_percentage']:.2f}%
            🎯 P&L: ₹{summary['total_pnl']:,.0f}
            
            📊 Quick Stats:
            • {len(PORTFOLIO_DATA['stocks'])} stocks
            • {len(set(stock['sector'] for stock in PORTFOLIO_DATA['stocks']))} sectors
            • {len(set(stock['country'] for stock in PORTFOLIO_DATA['stocks']))} countries
            
            {self._get_emoji_status(summary['total_pnl_percentage'])}
            """
        else:
            response = f"""
            Complete Portfolio Analysis:
            
            Portfolio Value: ₹{summary['total_value']:,.0f}
            Total Return: {summary['total_pnl_percentage']:.2f}%
            P&L: ₹{summary['total_pnl']:,.0f}
            
            Quick Stats:
            • {len(PORTFOLIO_DATA['stocks'])} stocks
            • {len(set(stock['sector'] for stock in PORTFOLIO_DATA['stocks']))} sectors
            • {len(set(stock['country'] for stock in PORTFOLIO_DATA['stocks']))} countries
            
            {self._get_performance_status(summary['total_pnl_percentage'])}
            """
        
        return {
            "agent": self.name,
            "response": response,
            "data": summary,
            "type": "comprehensive_analysis"
        }
    
    def _get_emoji_status(self, pnl_percentage: float) -> str:
        """Get emoji status based on performance"""
        if pnl_percentage > 20:
            return "🔥🔥🔥 AMAZING PERFORMANCE! 🔥🔥🔥"
        elif pnl_percentage > 10:
            return "🚀 Great job! Portfolio is killing it! 🚀"
        elif pnl_percentage > 0:
            return "✅ Good performance! Keep it up! ✅"
        else:
            return "😔 Tough market, but stay strong! 💪"
    
    def _get_performance_status(self, pnl_percentage: float) -> str:
        """Get performance status"""
        if pnl_percentage > 20:
            return "Excellent performance! Portfolio is performing exceptionally well."
        elif pnl_percentage > 10:
            return "Good performance! Portfolio is showing positive returns."
        elif pnl_percentage > 0:
            return "Positive performance! Portfolio is in the green."
        else:
            return "Portfolio is currently down, but markets are cyclical."
    
    def _get_performance_insight(self, pnl_percentage: float) -> str:
        """Get performance insight"""
        if pnl_percentage > 15:
            return "Your portfolio is outperforming most benchmarks!"
        elif pnl_percentage > 8:
            return "Solid performance with good diversification."
        elif pnl_percentage > 0:
            return "Positive returns, consider reviewing allocation."
        else:
            return "Consider reviewing your investment strategy."
    
    def _calculate_diversification_score(self, stocks: int, sectors: int, countries: int) -> int:
        """Calculate diversification score out of 10"""
        score = 0
        if stocks >= 10:
            score += 3
        elif stocks >= 5:
            score += 2
        else:
            score += 1
        
        if sectors >= 5:
            score += 4
        elif sectors >= 3:
            score += 3
        else:
            score += 1
        
        if countries >= 2:
            score += 3
        else:
            score += 1
        
        return min(score, 10)
    
    def _get_risk_insight(self, stocks: int, sectors: int, countries: int) -> str:
        """Get risk insight"""
        if stocks >= 10 and sectors >= 5 and countries >= 2:
            return "Excellent diversification! Low risk portfolio."
        elif stocks >= 5 and sectors >= 3:
            return "Good diversification. Moderate risk."
        else:
            return "Consider diversifying more to reduce risk."
    
    def _enlist_stocks(self, language: str) -> Dict[str, Any]:
        """List all stocks in the portfolio"""
        stocks = PORTFOLIO_DATA["stocks"]
        
        if language == "genz":
            response = f"📈 Your Stock Collection ({len(stocks)} stocks) 📈\n\n"
            for i, stock in enumerate(stocks, 1):
                pnl = (stock['current_price'] - stock['avg_price']) * stock['quantity']
                pnl_pct = ((stock['current_price'] - stock['avg_price']) / stock['avg_price']) * 100
                emoji = "🟢" if pnl >= 0 else "🔴"
                response += f"{i}. {emoji} {stock['name']} ({stock['symbol']})\n"
                response += f"   💰 Qty: {stock['quantity']} | Price: ₹{stock['current_price']:.2f}\n"
                response += f"   🏢 {stock['sector']} | 🌍 {stock['country']}\n"
                response += f"   📊 P&L: ₹{pnl:,.0f} ({pnl_pct:+.2f}%)\n\n"
        else:
            response = f"Portfolio Stocks ({len(stocks)} stocks):\n\n"
            for i, stock in enumerate(stocks, 1):
                pnl = (stock['current_price'] - stock['avg_price']) * stock['quantity']
                pnl_pct = ((stock['current_price'] - stock['avg_price']) / stock['avg_price']) * 100
                status = "▲" if pnl >= 0 else "▼"
                response += f"{i}. {status} {stock['name']} ({stock['symbol']})\n"
                response += f"   Quantity: {stock['quantity']} | Current Price: ₹{stock['current_price']:.2f}\n"
                response += f"   Sector: {stock['sector']} | Country: {stock['country']}\n"
                response += f"   P&L: ₹{pnl:,.0f} ({pnl_pct:+.2f}%)\n\n"
        
        return {
            "agent": self.name,
            "response": response + "📊 Source: Portfolio Analyzer Agent",
            "data": {"stocks": stocks, "total_stocks": len(stocks)},
            "type": "stocks_list"
        }
    
    def _enlist_sectors(self, language: str) -> Dict[str, Any]:
        """List all sectors in the portfolio"""
        sectors = {}
        for stock in PORTFOLIO_DATA["stocks"]:
            sector = stock["sector"]
            if sector not in sectors:
                sectors[sector] = {
                    "stocks": [],
                    "total_value": 0,
                    "total_investment": 0,
                    "stock_count": 0
                }
            sectors[sector]["stocks"].append(stock["name"])
            sectors[sector]["total_value"] += stock["quantity"] * stock["current_price"]
            sectors[sector]["total_investment"] += stock["quantity"] * stock["avg_price"]
            sectors[sector]["stock_count"] += 1
        
        # Calculate sector percentages
        total_portfolio_value = sum(s["total_value"] for s in sectors.values())
        
        if language == "genz":
            response = f"🏢 Your Sector Breakdown ({len(sectors)} sectors) 🏢\n\n"
            for i, (sector, data) in enumerate(sectors.items(), 1):
                pnl = data["total_value"] - data["total_investment"]
                pnl_pct = (pnl / data["total_investment"]) * 100 if data["total_investment"] > 0 else 0
                allocation_pct = (data["total_value"] / total_portfolio_value) * 100
                emoji = "🟢" if pnl >= 0 else "🔴"
                response += f"{i}. {emoji} {sector}\n"
                response += f"   💰 Value: ₹{data['total_value']:,.0f} ({allocation_pct:.1f}%)\n"
                response += f"   📊 Stocks: {data['stock_count']} | P&L: ₹{pnl:,.0f} ({pnl_pct:+.2f}%)\n"
                response += f"   🏢 Companies: {', '.join(data['stocks'][:3])}"
                if len(data['stocks']) > 3:
                    response += f" +{len(data['stocks'])-3} more"
                response += "\n\n"
        else:
            response = f"Portfolio Sectors ({len(sectors)} sectors):\n\n"
            for i, (sector, data) in enumerate(sectors.items(), 1):
                pnl = data["total_value"] - data["total_investment"]
                pnl_pct = (pnl / data["total_investment"]) * 100 if data["total_investment"] > 0 else 0
                allocation_pct = (data["total_value"] / total_portfolio_value) * 100
                status = "▲" if pnl >= 0 else "▼"
                response += f"{i}. {status} {sector}\n"
                response += f"   Value: ₹{data['total_value']:,.0f} ({allocation_pct:.1f}% of portfolio)\n"
                response += f"   Stocks: {data['stock_count']} | P&L: ₹{pnl:,.0f} ({pnl_pct:+.2f}%)\n"
                response += f"   Companies: {', '.join(data['stocks'][:3])}"
                if len(data['stocks']) > 3:
                    response += f" and {len(data['stocks'])-3} more"
                response += "\n\n"
        
        return {
            "agent": self.name,
            "response": response + "📊 Source: Portfolio Analyzer Agent",
            "data": {"sectors": sectors, "total_sectors": len(sectors)},
            "type": "sectors_list"
        }
    
    def _enlist_countries(self, language: str) -> Dict[str, Any]:
        """List all countries in the portfolio"""
        countries = {}
        for stock in PORTFOLIO_DATA["stocks"]:
            country = stock["country"]
            if country not in countries:
                countries[country] = {
                    "stocks": [],
                    "sectors": set(),
                    "total_value": 0,
                    "total_investment": 0,
                    "stock_count": 0
                }
            countries[country]["stocks"].append(stock["name"])
            countries[country]["sectors"].add(stock["sector"])
            countries[country]["total_value"] += stock["quantity"] * stock["current_price"]
            countries[country]["total_investment"] += stock["quantity"] * stock["avg_price"]
            countries[country]["stock_count"] += 1
        
        # Calculate country percentages
        total_portfolio_value = sum(c["total_value"] for c in countries.values())
        
        if language == "genz":
            response = f"🌍 Your Geographic Breakdown ({len(countries)} countries) 🌍\n\n"
            for i, (country, data) in enumerate(countries.items(), 1):
                pnl = data["total_value"] - data["total_investment"]
                pnl_pct = (pnl / data["total_investment"]) * 100 if data["total_investment"] > 0 else 0
                allocation_pct = (data["total_value"] / total_portfolio_value) * 100
                emoji = "🟢" if pnl >= 0 else "🔴"
                flag = "🇮🇳" if country == "India" else "🇺🇸"
                response += f"{i}. {emoji} {flag} {country}\n"
                response += f"   💰 Value: ₹{data['total_value']:,.0f} ({allocation_pct:.1f}%)\n"
                response += f"   📊 Stocks: {data['stock_count']} | Sectors: {len(data['sectors'])}\n"
                response += f"   📈 P&L: ₹{pnl:,.0f} ({pnl_pct:+.2f}%)\n"
                response += f"   🏢 Top Companies: {', '.join(data['stocks'][:3])}"
                if len(data['stocks']) > 3:
                    response += f" +{len(data['stocks'])-3} more"
                response += "\n\n"
        else:
            response = f"Portfolio Countries ({len(countries)} countries):\n\n"
            for i, (country, data) in enumerate(countries.items(), 1):
                pnl = data["total_value"] - data["total_investment"]
                pnl_pct = (pnl / data["total_investment"]) * 100 if data["total_investment"] > 0 else 0
                allocation_pct = (data["total_value"] / total_portfolio_value) * 100
                status = "▲" if pnl >= 0 else "▼"
                response += f"{i}. {status} {country}\n"
                response += f"   Value: ₹{data['total_value']:,.0f} ({allocation_pct:.1f}% of portfolio)\n"
                response += f"   Stocks: {data['stock_count']} | Sectors: {len(data['sectors'])}\n"
                response += f"   P&L: ₹{pnl:,.0f} ({pnl_pct:+.2f}%)\n"
                response += f"   Companies: {', '.join(data['stocks'][:3])}"
                if len(data['stocks']) > 3:
                    response += f" and {len(data['stocks'])-3} more"
                response += "\n\n"
        
        return {
            "agent": self.name,
            "response": response + "📊 Source: Portfolio Analyzer Agent",
            "data": {"countries": countries, "total_countries": len(countries)},
            "type": "countries_list"
        }

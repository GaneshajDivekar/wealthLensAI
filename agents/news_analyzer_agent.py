from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from data.portfolio_data import PORTFOLIO_DATA, SECTORS, COUNTRIES
import requests
from datetime import datetime, timedelta
import json

class NewsAnalyzerAgent(BaseAgent):
    """Agent for analyzing news and its impact on portfolio"""
    
    def __init__(self):
        super().__init__(
            name="News Analyzer",
            description="Analyzes market news and provides insights on portfolio impact"
        )
        self.news_cache = {}
        self.cache_duration = 3600  # 1 hour
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process news analysis request"""
        query = input_data.get("query", "").lower()
        user_language = input_data.get("language", "normal")
        
        if "news" in query and "impact" in query:
            return self._analyze_news_impact(user_language)
        
        elif "traffic" in query and ("india" in query or "usa" in query):
            return self._analyze_traffic_impact(query, user_language)
        
        elif "market" in query and "news" in query:
            return self._get_market_news(user_language)
        
        elif "sector" in query and "news" in query:
            return self._get_sector_news(query, user_language)
        
        else:
            return self._get_general_news_analysis(user_language)
    
    def _analyze_news_impact(self, language: str) -> Dict[str, Any]:
        """Analyze news impact on portfolio"""
        # Simulate news impact analysis
        impact_analysis = {
            "positive_impact": ["Technology", "Banking"],
            "negative_impact": ["Oil & Gas"],
            "neutral_impact": ["Consumer Discretionary", "Automotive"],
            "key_events": [
                "Tech stocks rally on AI breakthrough news",
                "Banking sector stable despite rate changes",
                "Oil prices volatile due to geopolitical tensions"
            ]
        }
        
        if language == "genz":
            response = f"""
            📰 News Impact Analysis 📰
            
            🟢 Positive Impact Sectors:
            {', '.join(impact_analysis['positive_impact'])}
            
            🔴 Negative Impact Sectors:
            {', '.join(impact_analysis['negative_impact'])}
            
            🟡 Neutral Sectors:
            {', '.join(impact_analysis['neutral_impact'])}
            
            📊 Key Events:
            """
            for event in impact_analysis['key_events']:
                response += f"• {event}\n"
        else:
            response = f"""
            News Impact Analysis:
            
            Positive Impact Sectors:
            {', '.join(impact_analysis['positive_impact'])}
            
            Negative Impact Sectors:
            {', '.join(impact_analysis['negative_impact'])}
            
            Neutral Sectors:
            {', '.join(impact_analysis['neutral_impact'])}
            
            Key Events:
            """
            for event in impact_analysis['key_events']:
                response += f"• {event}\n"
        
        return {
            "agent": self.name,
            "response": response + "\n\n📰 Source: News Analyzer Agent",
            "data": impact_analysis,
            "type": "news_impact_analysis"
        }
    
    def _analyze_traffic_impact(self, query: str, language: str) -> Dict[str, Any]:
        """Analyze traffic issues impact on stocks"""
        affected_stocks = []
        
        if "india" in query:
            affected_stocks = [
                {"symbol": "RELIANCE.NS", "name": "Reliance Industries", "impact": "High - Logistics affected"},
                {"symbol": "TCS.NS", "name": "TCS", "impact": "Medium - Delivery delays"},
                {"symbol": "INFY.NS", "name": "Infosys", "impact": "Medium - Project timelines"},
                {"symbol": "HDFCBANK.NS", "name": "HDFC Bank", "impact": "Low - Digital banking continues"}
            ]
        elif "usa" in query:
            affected_stocks = [
                {"symbol": "AMZN", "name": "Amazon", "impact": "High - Delivery network affected"},
                {"symbol": "TSLA", "name": "Tesla", "impact": "Medium - Supply chain delays"},
                {"symbol": "AAPL", "name": "Apple", "impact": "Medium - Product delivery"},
                {"symbol": "MSFT", "name": "Microsoft", "impact": "Low - Cloud services stable"}
            ]
        
        if language == "genz":
            response = f"""
            🚦 Traffic Impact Analysis 🚦
            
            📍 Affected Region: {'India 🇮🇳' if 'india' in query else 'USA 🇺🇸'}
            
            📊 Stocks Affected:
            """
            for stock in affected_stocks:
                emoji = "🔴" if "High" in stock["impact"] else "🟡" if "Medium" in stock["impact"] else "🟢"
                response += f"{emoji} {stock['name']} ({stock['symbol']}): {stock['impact']}\n"
        else:
            response = f"""
            Traffic Impact Analysis:
            
            Affected Region: {'India' if 'india' in query else 'USA'}
            
            Stocks Affected:
            """
            for stock in affected_stocks:
                response += f"• {stock['name']} ({stock['symbol']}): {stock['impact']}\n"
        
        return {
            "agent": self.name,
            "response": response,
            "data": {"affected_stocks": affected_stocks, "region": "India" if "india" in query else "USA"},
            "type": "traffic_impact_analysis"
        }
    
    def _get_market_news(self, language: str) -> Dict[str, Any]:
        """Get market news"""
        market_news = [
            {
                "headline": "Tech stocks surge on AI breakthrough",
                "impact": "positive",
                "sectors": ["Technology"],
                "stocks": ["AAPL", "MSFT", "GOOGL", "TCS.NS", "INFY.NS"]
            },
            {
                "headline": "Banking sector stable despite rate changes",
                "impact": "neutral",
                "sectors": ["Banking"],
                "stocks": ["HDFCBANK.NS", "ICICIBANK.NS", "YESBANK.NS"]
            },
            {
                "headline": "Oil prices volatile due to geopolitical tensions",
                "impact": "negative",
                "sectors": ["Oil & Gas"],
                "stocks": ["RELIANCE.NS"]
            }
        ]
        
        if language == "genz":
            response = "📰 Latest Market News 📰\n\n"
            for news in market_news:
                emoji = "🟢" if news["impact"] == "positive" else "🔴" if news["impact"] == "negative" else "🟡"
                response += f"{emoji} {news['headline']}\n"
        else:
            response = "Latest Market News:\n\n"
            for news in market_news:
                response += f"• {news['headline']}\n"
        
        return {
            "agent": self.name,
            "response": response,
            "data": market_news,
            "type": "market_news"
        }
    
    def _get_sector_news(self, query: str, language: str) -> Dict[str, Any]:
        """Get sector-specific news"""
        sector_news = {
            "technology": [
                "AI breakthrough drives tech stock rally",
                "Cloud computing adoption accelerates",
                "Cybersecurity concerns rise"
            ],
            "banking": [
                "Interest rate changes impact banking sector",
                "Digital banking adoption increases",
                "Regulatory changes affect compliance"
            ],
            "oil & gas": [
                "Geopolitical tensions affect oil prices",
                "Renewable energy transition accelerates",
                "Supply chain disruptions impact operations"
            ]
        }
        
        # Find relevant sector
        relevant_sector = None
        for sector in sector_news.keys():
            if sector in query:
                relevant_sector = sector
                break
        
        if not relevant_sector:
            relevant_sector = "technology"  # default
        
        news_list = sector_news.get(relevant_sector, [])
        
        if language == "genz":
            response = f"📰 {relevant_sector.title()} Sector News 📰\n\n"
            for news in news_list:
                response += f"📊 {news}\n"
        else:
            response = f"{relevant_sector.title()} Sector News:\n\n"
            for news in news_list:
                response += f"• {news}\n"
        
        return {
            "agent": self.name,
            "response": response,
            "data": {"sector": relevant_sector, "news": news_list},
            "type": "sector_news"
        }
    
    def _get_general_news_analysis(self, language: str) -> Dict[str, Any]:
        """Get general news analysis"""
        analysis = {
            "market_sentiment": "Bullish",
            "key_drivers": [
                "AI and technology innovation",
                "Strong corporate earnings",
                "Economic recovery signals"
            ],
            "risks": [
                "Geopolitical tensions",
                "Inflation concerns",
                "Supply chain disruptions"
            ],
            "recommendations": [
                "Maintain technology exposure",
                "Diversify across sectors",
                "Monitor geopolitical developments"
            ]
        }
        
        if language == "genz":
            response = f"""
            📊 General Market Analysis 📊
            
            🎯 Market Sentiment: {analysis['market_sentiment']} 📈
            
            🚀 Key Drivers:
            """
            for driver in analysis['key_drivers']:
                response += f"• {driver}\n"
            
            response += "\n⚠️ Risks:\n"
            for risk in analysis['risks']:
                response += f"• {risk}\n"
            
            response += "\n💡 Recommendations:\n"
            for rec in analysis['recommendations']:
                response += f"• {rec}\n"
        else:
            response = f"""
            General Market Analysis:
            
            Market Sentiment: {analysis['market_sentiment']}
            
            Key Drivers:
            """
            for driver in analysis['key_drivers']:
                response += f"• {driver}\n"
            
            response += "\nRisks:\n"
            for risk in analysis['risks']:
                response += f"• {risk}\n"
            
            response += "\nRecommendations:\n"
            for rec in analysis['recommendations']:
                response += f"• {rec}\n"
        
        return {
            "agent": self.name,
            "response": response,
            "data": analysis,
            "type": "general_news_analysis"
        }
    
    def _fetch_news_api(self, query: str = "financial markets") -> List[Dict]:
        """Fetch news from API (simulated)"""
        # Simulate API call
        return [
            {
                "title": "Tech stocks rally on AI breakthrough",
                "description": "Major technology companies see significant gains",
                "published_at": datetime.now().isoformat()
            },
            {
                "title": "Banking sector remains stable",
                "description": "Financial institutions show resilience",
                "published_at": datetime.now().isoformat()
            }
        ]

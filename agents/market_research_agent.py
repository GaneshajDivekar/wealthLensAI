from typing import Dict, Any
from agents.base_agent import BaseAgent
from data.portfolio_data import get_portfolio_data
import random

class MarketResearchAgent(BaseAgent):
    """Agent for conducting market research and industry analysis"""
    
    def __init__(self):
        super().__init__(
            name="Market Research",
            description="Conducts market research and provides industry insights"
        )
        
        # Market research data (simulated)
        self.market_data = {
            "Technology": {
                "growth_rate": 0.12,
                "trend": "Bullish",
                "key_drivers": ["AI/ML", "Cloud Computing", "Cybersecurity"],
                "risks": ["Regulation", "Competition", "Economic Downturn"]
            },
            "Healthcare": {
                "growth_rate": 0.08,
                "trend": "Stable",
                "key_drivers": ["Biotech", "Digital Health", "Aging Population"],
                "risks": ["Regulation", "Patent Expiry", "Pricing Pressure"]
            },
            "Finance": {
                "growth_rate": 0.06,
                "trend": "Moderate",
                "key_drivers": ["Fintech", "Digital Banking", "ESG Investing"],
                "risks": ["Interest Rates", "Regulation", "Cybersecurity"]
            },
            "Consumer": {
                "growth_rate": 0.04,
                "trend": "Stable",
                "key_drivers": ["E-commerce", "Sustainability", "Personalization"],
                "risks": ["Inflation", "Supply Chain", "Consumer Spending"]
            },
            "Energy": {
                "growth_rate": 0.03,
                "trend": "Transition",
                "key_drivers": ["Renewables", "EV Adoption", "Energy Storage"],
                "risks": ["Policy Changes", "Commodity Prices", "Technology Disruption"]
            }
        }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process market research request"""
        query = input_data.get("query", "")
        user_language = input_data.get("language", "normal")
        
        try:
            # Extract sectors from portfolio
            portfolio_sectors = self._get_portfolio_sectors()
            
            # Conduct market research
            market_analysis = self._conduct_market_research(portfolio_sectors)
            
            # Generate response based on language preference
            response = self._format_market_response(market_analysis, user_language)
            
            return {
                "agent": self.name,
                "response": response + "\n\n🔍 Source: Market Research Agent",
                "data": market_analysis,
                "type": "market_research"
            }
            
        except Exception as e:
            print(f"Error in market research: {e}")
            return {
                "agent": self.name,
                "response": "Sorry, I couldn't conduct market research at the moment.",
                "data": {"error": str(e)},
                "type": "error"
            }
    
    def _get_portfolio_sectors(self) -> list:
        """Get sectors from portfolio"""
        portfolio_data = get_portfolio_data()
        sectors = list(set(stock['sector'] for stock in portfolio_data['stocks']))
        return sectors
    
    def _conduct_market_research(self, sectors: list) -> Dict[str, Any]:
        """Conduct market research for given sectors"""
        research_results = {}
        
        for sector in sectors:
            if sector in self.market_data:
                sector_data = self.market_data[sector]
                research_results[sector] = {
                    "growth_rate": sector_data["growth_rate"],
                    "trend": sector_data["trend"],
                    "key_drivers": sector_data["key_drivers"],
                    "risks": sector_data["risks"],
                    "outlook": self._generate_sector_outlook(sector_data),
                    "recommendations": self._generate_sector_recommendations(sector_data)
                }
            else:
                # Generate generic data for unknown sectors
                research_results[sector] = {
                    "growth_rate": random.uniform(0.02, 0.10),
                    "trend": random.choice(["Bullish", "Stable", "Bearish"]),
                    "key_drivers": ["Innovation", "Market Demand", "Global Trends"],
                    "risks": ["Competition", "Economic Factors", "Regulation"],
                    "outlook": "Moderate growth expected with some volatility",
                    "recommendations": ["Monitor sector performance", "Diversify within sector"]
                }
        
        # Overall market analysis
        overall_analysis = self._generate_overall_analysis(research_results)
        
        return {
            "sector_analysis": research_results,
            "overall_analysis": overall_analysis,
            "market_trends": self._get_market_trends(),
            "investment_themes": self._get_investment_themes()
        }
    
    def _generate_sector_outlook(self, sector_data: Dict[str, Any]) -> str:
        """Generate sector outlook based on data"""
        growth_rate = sector_data["growth_rate"]
        trend = sector_data["trend"]
        
        if growth_rate > 0.08 and trend == "Bullish":
            return "Strong growth potential with positive momentum"
        elif growth_rate > 0.05:
            return "Moderate growth with stable fundamentals"
        else:
            return "Slower growth but potential for value opportunities"
    
    def _generate_sector_recommendations(self, sector_data: Dict[str, Any]) -> list:
        """Generate recommendations for sector"""
        recommendations = []
        
        if sector_data["trend"] == "Bullish":
            recommendations.append("Consider increasing exposure to high-growth areas")
            recommendations.append("Focus on companies with strong competitive advantages")
        elif sector_data["trend"] == "Bearish":
            recommendations.append("Reduce exposure or focus on defensive positions")
            recommendations.append("Look for value opportunities in beaten-down stocks")
        else:
            recommendations.append("Maintain balanced exposure")
            recommendations.append("Focus on quality companies with strong fundamentals")
        
        return recommendations
    
    def _generate_overall_analysis(self, sector_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall market analysis"""
        avg_growth = sum(analysis["growth_rate"] for analysis in sector_analysis.values()) / len(sector_analysis)
        
        bullish_sectors = sum(1 for analysis in sector_analysis.values() if analysis["trend"] == "Bullish")
        total_sectors = len(sector_analysis)
        
        if bullish_sectors / total_sectors > 0.6:
            overall_sentiment = "Positive"
        elif bullish_sectors / total_sectors > 0.3:
            overall_sentiment = "Neutral"
        else:
            overall_sentiment = "Cautious"
        
        return {
            "average_growth": avg_growth,
            "sentiment": overall_sentiment,
            "bullish_sectors": bullish_sectors,
            "total_sectors": total_sectors,
            "key_insights": [
                "Technology and Healthcare showing strong growth potential",
                "Energy sector in transition phase with opportunities",
                "Consumer sector stable but sensitive to economic conditions"
            ]
        }
    
    def _get_market_trends(self) -> list:
        """Get current market trends"""
        return [
            "AI and Machine Learning driving technology growth",
            "ESG investing gaining momentum",
            "Digital transformation across industries",
            "Supply chain resilience becoming priority",
            "Renewable energy adoption accelerating"
        ]
    
    def _get_investment_themes(self) -> list:
        """Get investment themes"""
        return [
            "Digital Transformation",
            "Sustainability & ESG",
            "Healthcare Innovation",
            "Fintech Disruption",
            "Clean Energy Transition"
        ]
    
    def _format_market_response(self, market_analysis: Dict[str, Any], language: str) -> str:
        """Format market research response based on language preference"""
        if language == "genz":
            return self._format_genz_market_response(market_analysis)
        else:
            return self._format_normal_market_response(market_analysis)
    
    def _format_genz_market_response(self, market_analysis: Dict[str, Any]) -> str:
        """Format market response in Gen Z style"""
        overall = market_analysis["overall_analysis"]
        
        response = f"""
        🔍 MARKET RESEARCH REPORT 🔍
        
        📊 Overall Sentiment: {overall['sentiment']} 
        📈 Average Growth: {overall['average_growth']:.2%}
        🚀 Bullish Sectors: {overall['bullish_sectors']}/{overall['total_sectors']}
        
        🎯 SECTOR BREAKDOWN:
        """
        
        for sector, analysis in market_analysis["sector_analysis"].items():
            emoji = "🚀" if analysis["trend"] == "Bullish" else "📊" if analysis["trend"] == "Stable" else "⚠️"
            response += f"{emoji} {sector}: {analysis['trend']} ({analysis['growth_rate']:.2%} growth)\n"
        
        response += "\n💡 KEY INSIGHTS:\n"
        for insight in overall["key_insights"]:
            response += f"• {insight}\n"
        
        response += "\n🔥 HOT TRENDS:\n"
        for trend in market_analysis["market_trends"][:3]:
            response += f"• {trend}\n"
        
        return response
    
    def _format_normal_market_response(self, market_analysis: Dict[str, Any]) -> str:
        """Format market response in normal style"""
        overall = market_analysis["overall_analysis"]
        
        response = f"""
        Market Research Report
        
        Overall Sentiment: {overall['sentiment']}
        Average Growth Rate: {overall['average_growth']:.2%}
        Bullish Sectors: {overall['bullish_sectors']}/{overall['total_sectors']}
        
        Sector Analysis:
        """
        
        for sector, analysis in market_analysis["sector_analysis"].items():
            response += f"• {sector}: {analysis['trend']} ({analysis['growth_rate']:.2%} growth)\n"
            response += f"  Outlook: {analysis['outlook']}\n"
        
        response += "\nKey Insights:\n"
        for insight in overall["key_insights"]:
            response += f"• {insight}\n"
        
        response += "\nMarket Trends:\n"
        for trend in market_analysis["market_trends"][:3]:
            response += f"• {trend}\n"
        
        return response

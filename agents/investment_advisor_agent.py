from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from data.portfolio_data import PORTFOLIO_DATA, get_portfolio_summary, get_stocks_by_criteria
import random

class InvestmentAdvisorAgent(BaseAgent):
    """Agent for providing investment advice and recommendations"""
    
    def __init__(self):
        super().__init__(
            name="Investment Advisor",
            description="Provides buy/sell/hold recommendations and investment advice"
        )
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process investment advice request"""
        query = input_data.get("query", "").lower()
        user_language = input_data.get("language", "normal")
        
        if "buy" in query or "invest" in query:
            return self._generate_buy_recommendations(user_language)
        
        elif "sell" in query:
            return self._generate_sell_recommendations(user_language)
        
        elif "hold" in query or "holdings" in query:
            return self._generate_hold_recommendations(user_language)
        
        elif "recommendation" in query or "advice" in query:
            return self._generate_general_recommendations(user_language)
        
        elif "where" in query and "invest" in query:
            return self._generate_investment_opportunities(user_language)
        
        else:
            return self._generate_comprehensive_advice(user_language)
    
    def _generate_buy_recommendations(self, language: str) -> Dict[str, Any]:
        """Generate buy recommendations"""
        buy_recommendations = [
            {
                "symbol": "AAPL",
                "name": "Apple Inc",
                "reason": "Strong AI integration and ecosystem growth",
                "target_price": 200,
                "confidence": "High"
            },
            {
                "symbol": "MSFT",
                "name": "Microsoft Corporation",
                "reason": "Cloud computing leadership and AI innovation",
                "target_price": 350,
                "confidence": "High"
            },
            {
                "symbol": "TCS.NS",
                "name": "Tata Consultancy Services",
                "reason": "Digital transformation demand and global expansion",
                "target_price": 4200,
                "confidence": "Medium"
            },
            {
                "symbol": "SUZLON.NS",
                "name": "Suzlon Energy",
                "reason": "Renewable energy growth and government support",
                "target_price": 12,
                "confidence": "Medium"
            }
        ]
        
        if language == "genz":
            response = "🛒 BUY Recommendations 🛒\n\n"
            for rec in buy_recommendations:
                confidence_emoji = "🟢" if rec["confidence"] == "High" else "🟡"
                response += f"""
                {confidence_emoji} {rec['name']} ({rec['symbol']})
                💰 Target: ₹{rec['target_price']}
                📈 Reason: {rec['reason']}
                """
        else:
            response = "Buy Recommendations:\n\n"
            for rec in buy_recommendations:
                response += f"""
                {rec['name']} ({rec['symbol']})
                Target Price: ₹{rec['target_price']}
                Reason: {rec['reason']}
                Confidence: {rec['confidence']}
                """
        
        return {
            "agent": self.name,
            "response": response + "\n\n💡 Source: Investment Advisor Agent",
            "data": buy_recommendations,
            "type": "buy_recommendations"
        }
    
    def _generate_sell_recommendations(self, language: str) -> Dict[str, Any]:
        """Generate sell recommendations"""
        sell_recommendations = [
            {
                "symbol": "RELIANCE.NS",
                "name": "Reliance Industries",
                "reason": "Oil price volatility and regulatory concerns",
                "current_price": 2650,
                "suggested_price": 2400,
                "urgency": "Medium"
            },
            {
                "symbol": "JPASSOCIAT.NS",
                "name": "Jaiprakash Associates",
                "reason": "High debt levels and sector challenges",
                "current_price": 6.2,
                "suggested_price": 5.5,
                "urgency": "High"
            }
        ]
        
        if language == "genz":
            response = "📉 SELL Recommendations 📉\n\n"
            for rec in sell_recommendations:
                urgency_emoji = "🔴" if rec["urgency"] == "High" else "🟡"
                response += f"""
                {urgency_emoji} {rec['name']} ({rec['symbol']})
                💰 Current: ₹{rec['current_price']} → Suggested: ₹{rec['suggested_price']}
                📉 Reason: {rec['reason']}
                """
        else:
            response = "Sell Recommendations:\n\n"
            for rec in sell_recommendations:
                response += f"""
                {rec['name']} ({rec['symbol']})
                Current Price: ₹{rec['current_price']}
                Suggested Price: ₹{rec['suggested_price']}
                Reason: {rec['reason']}
                Urgency: {rec['urgency']}
                """
        
        return {
            "agent": self.name,
            "response": response + "\n\n💡 Source: Investment Advisor Agent",
            "data": sell_recommendations,
            "type": "sell_recommendations"
        }
    
    def _generate_hold_recommendations(self, language: str) -> Dict[str, Any]:
        """Generate hold recommendations"""
        hold_recommendations = [
            {
                "symbol": "HDFCBANK.NS",
                "name": "HDFC Bank",
                "reason": "Strong fundamentals and stable growth",
                "expected_return": "8-12%",
                "timeframe": "6-12 months"
            },
            {
                "symbol": "INFY.NS",
                "name": "Infosys",
                "reason": "Consistent performance and dividend yield",
                "expected_return": "10-15%",
                "timeframe": "6-12 months"
            },
            {
                "symbol": "GOOGL",
                "name": "Alphabet Inc",
                "reason": "AI leadership and advertising recovery",
                "expected_return": "15-20%",
                "timeframe": "12-18 months"
            }
        ]
        
        if language == "genz":
            response = "🤝 HOLD Recommendations 🤝\n\n"
            for rec in hold_recommendations:
                response += f"""
                🟢 {rec['name']} ({rec['symbol']})
                📈 Expected Return: {rec['expected_return']}
                ⏰ Timeframe: {rec['timeframe']}
                💡 Reason: {rec['reason']}
                """
        else:
            response = "Hold Recommendations:\n\n"
            for rec in hold_recommendations:
                response += f"""
                {rec['name']} ({rec['symbol']})
                Expected Return: {rec['expected_return']}
                Timeframe: {rec['timeframe']}
                Reason: {rec['reason']}
                """
        
        return {
            "agent": self.name,
            "response": response + "\n\n💡 Source: Investment Advisor Agent",
            "data": hold_recommendations,
            "type": "hold_recommendations"
        }
    
    def _generate_investment_opportunities(self, language: str) -> Dict[str, Any]:
        """Generate investment opportunities"""
        opportunities = [
            {
                "sector": "Technology",
                "opportunities": [
                    "AI and Machine Learning companies",
                    "Cloud computing providers",
                    "Cybersecurity firms"
                ],
                "reason": "Digital transformation acceleration",
                "risk_level": "Medium"
            },
            {
                "sector": "Renewable Energy",
                "opportunities": [
                    "Solar energy companies",
                    "Wind power providers",
                    "Energy storage solutions"
                ],
                "reason": "Government support and sustainability focus",
                "risk_level": "Medium-High"
            },
            {
                "sector": "Healthcare",
                "opportunities": [
                    "Biotechnology companies",
                    "Digital health platforms",
                    "Pharmaceutical research"
                ],
                "reason": "Aging population and innovation",
                "risk_level": "High"
            }
        ]
        
        if language == "genz":
            response = "💡 Investment Opportunities 💡\n\n"
            for opp in opportunities:
                risk_emoji = "🟢" if opp["risk_level"] == "Low" else "🟡" if opp["risk_level"] == "Medium" else "🔴"
                response += f"""
                {risk_emoji} {opp['sector']} Sector
                🎯 Opportunities: {', '.join(opp['opportunities'])}
                💡 Reason: {opp['reason']}
                ⚠️ Risk: {opp['risk_level']}
                """
        else:
            response = "Investment Opportunities:\n\n"
            for opp in opportunities:
                response += f"""
                {opp['sector']} Sector:
                Opportunities: {', '.join(opp['opportunities'])}
                Reason: {opp['reason']}
                Risk Level: {opp['risk_level']}
                """
        
        return {
            "agent": self.name,
            "response": response,
            "data": opportunities,
            "type": "investment_opportunities"
        }
    
    def _generate_general_recommendations(self, language: str) -> Dict[str, Any]:
        """Generate general investment recommendations"""
        recommendations = {
            "portfolio_allocation": {
                "large_cap": "40%",
                "mid_cap": "30%",
                "small_cap": "20%",
                "international": "10%"
            },
            "sector_allocation": {
                "technology": "30%",
                "banking": "25%",
                "consumer": "20%",
                "energy": "15%",
                "others": "10%"
            },
            "risk_management": [
                "Maintain 6-month emergency fund",
                "Diversify across sectors and geographies",
                "Regular portfolio rebalancing",
                "Monitor market conditions"
            ]
        }
        
        if language == "genz":
            response = f"""
            📊 Investment Strategy 📊
            
            💰 Portfolio Allocation:
            • Large Cap: {recommendations['portfolio_allocation']['large_cap']}
            • Mid Cap: {recommendations['portfolio_allocation']['mid_cap']}
            • Small Cap: {recommendations['portfolio_allocation']['small_cap']}
            • International: {recommendations['portfolio_allocation']['international']}
            
            🏢 Sector Allocation:
            • Technology: {recommendations['sector_allocation']['technology']}
            • Banking: {recommendations['sector_allocation']['banking']}
            • Consumer: {recommendations['sector_allocation']['consumer']}
            • Energy: {recommendations['sector_allocation']['energy']}
            • Others: {recommendations['sector_allocation']['others']}
            
            ⚠️ Risk Management:
            """
            for risk in recommendations['risk_management']:
                response += f"• {risk}\n"
        else:
            response = f"""
            Investment Strategy:
            
            Portfolio Allocation:
            • Large Cap: {recommendations['portfolio_allocation']['large_cap']}
            • Mid Cap: {recommendations['portfolio_allocation']['mid_cap']}
            • Small Cap: {recommendations['portfolio_allocation']['small_cap']}
            • International: {recommendations['portfolio_allocation']['international']}
            
            Sector Allocation:
            • Technology: {recommendations['sector_allocation']['technology']}
            • Banking: {recommendations['sector_allocation']['banking']}
            • Consumer: {recommendations['sector_allocation']['consumer']}
            • Energy: {recommendations['sector_allocation']['energy']}
            • Others: {recommendations['sector_allocation']['others']}
            
            Risk Management:
            """
            for risk in recommendations['risk_management']:
                response += f"• {risk}\n"
        
        return {
            "agent": self.name,
            "response": response,
            "data": recommendations,
            "type": "general_recommendations"
        }
    
    def _generate_comprehensive_advice(self, language: str) -> Dict[str, Any]:
        """Generate comprehensive investment advice"""
        summary = get_portfolio_summary()
        
        # Generate personalized advice based on portfolio performance
        if summary['total_pnl_percentage'] > 15:
            advice = "Your portfolio is performing excellently! Consider taking some profits and rebalancing."
        elif summary['total_pnl_percentage'] > 5:
            advice = "Good performance! Focus on maintaining diversification and monitoring positions."
        else:
            advice = "Consider reviewing your investment strategy and potentially rebalancing your portfolio."
        
        if language == "genz":
            response = f"""
            🎯 Comprehensive Investment Advice 🎯
            
            📊 Current Performance: {summary['total_pnl_percentage']:.2f}%
            
            💡 Personalized Advice:
            {advice}
            
            🚀 Action Items:
            • Review portfolio allocation monthly
            • Monitor sector performance
            • Consider new opportunities in emerging sectors
            • Maintain emergency fund
            """
        else:
            response = f"""
            Comprehensive Investment Advice:
            
            Current Performance: {summary['total_pnl_percentage']:.2f}%
            
            Personalized Advice:
            {advice}
            
            Action Items:
            • Review portfolio allocation monthly
            • Monitor sector performance
            • Consider new opportunities in emerging sectors
            • Maintain emergency fund
            """
        
        return {
            "agent": self.name,
            "response": response,
            "data": {"performance": summary, "advice": advice},
            "type": "comprehensive_advice"
        }

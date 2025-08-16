from typing import Dict, Any
from agents.base_agent import BaseAgent
from data.portfolio_data import get_portfolio_data, get_portfolio_summary
import random

class RiskAnalyzerAgent(BaseAgent):
    """Agent for analyzing portfolio risk and providing risk management advice"""
    
    def __init__(self):
        super().__init__(
            name="Risk Analyzer",
            description="Analyzes portfolio risk and provides risk management recommendations"
        )
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process risk analysis request"""
        query = input_data.get("query", "")
        user_language = input_data.get("language", "normal")
        
        try:
            # Analyze portfolio risk
            risk_analysis = self._analyze_portfolio_risk()
            
            # Generate response based on language preference
            response = self._format_risk_response(risk_analysis, user_language)
            
            return {
                "agent": self.name,
                "response": response + "\n\n⚠️ Source: Risk Analyzer Agent",
                "data": risk_analysis,
                "type": "risk_analysis"
            }
            
        except Exception as e:
            print(f"Error in risk analyzer: {e}")
            return {
                "agent": self.name,
                "response": "Sorry, I couldn't analyze the risk at the moment.",
                "data": {"error": str(e)},
                "type": "error"
            }
    
    def _analyze_portfolio_risk(self) -> Dict[str, Any]:
        """Analyze portfolio risk metrics"""
        portfolio_data = get_portfolio_data()
        
        # Calculate risk metrics
        total_value = sum(stock['quantity'] * stock['current_price'] for stock in portfolio_data['stocks'])
        total_investment = sum(stock['quantity'] * stock['avg_price'] for stock in portfolio_data['stocks'])
        
        # Calculate volatility (simulated)
        volatility = random.uniform(0.15, 0.35)
        
        # Calculate sector concentration
        sectors = {}
        for stock in portfolio_data['stocks']:
            sector = stock['sector']
            current_value = stock['quantity'] * stock['current_price']
            sectors[sector] = sectors.get(sector, 0) + current_value
        
        max_sector_concentration = max(sectors.values()) / total_value if sectors else 0
        
        # Calculate country concentration
        countries = {}
        for stock in portfolio_data['stocks']:
            country = stock['country']
            current_value = stock['quantity'] * stock['current_price']
            countries[country] = countries.get(country, 0) + current_value
        
        max_country_concentration = max(countries.values()) / total_value if countries else 0
        
        # Risk assessment
        risk_score = self._calculate_risk_score(volatility, max_sector_concentration, max_country_concentration)
        risk_level = self._get_risk_level(risk_score)
        
        return {
            "total_value": total_value,
            "total_investment": total_investment,
            "volatility": volatility,
            "sector_concentration": max_sector_concentration,
            "country_concentration": max_country_concentration,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "sectors": sectors,
            "countries": countries,
            "recommendations": self._generate_risk_recommendations(risk_score, sectors, countries)
        }
    
    def _calculate_risk_score(self, volatility: float, sector_concentration: float, country_concentration: float) -> float:
        """Calculate overall risk score"""
        # Weighted risk factors
        volatility_weight = 0.4
        sector_weight = 0.3
        country_weight = 0.3
        
        risk_score = (
            volatility * volatility_weight +
            sector_concentration * sector_weight +
            country_concentration * country_weight
        )
        
        return min(risk_score, 1.0)  # Cap at 1.0
    
    def _get_risk_level(self, risk_score: float) -> str:
        """Get risk level based on risk score"""
        if risk_score < 0.3:
            return "Low"
        elif risk_score < 0.6:
            return "Medium"
        else:
            return "High"
    
    def _generate_risk_recommendations(self, risk_score: float, sectors: Dict[str, float], countries: Dict[str, float]) -> list:
        """Generate risk management recommendations"""
        recommendations = []
        
        if risk_score > 0.6:
            recommendations.append("Consider reducing portfolio concentration in high-risk sectors")
            recommendations.append("Diversify across more countries to reduce geopolitical risk")
            recommendations.append("Consider adding defensive stocks or bonds")
        
        if risk_score > 0.4:
            recommendations.append("Monitor sector concentration - consider rebalancing")
            recommendations.append("Review penny stock exposure and consider reducing if too high")
        
        if risk_score < 0.3:
            recommendations.append("Portfolio appears well-diversified")
            recommendations.append("Consider adding growth opportunities if risk tolerance allows")
        
        return recommendations
    
    def _format_risk_response(self, risk_analysis: Dict[str, Any], language: str) -> str:
        """Format risk analysis response based on language preference"""
        if language == "genz":
            return self._format_genz_risk_response(risk_analysis)
        else:
            return self._format_normal_risk_response(risk_analysis)
    
    def _format_genz_risk_response(self, risk_analysis: Dict[str, Any]) -> str:
        """Format risk response in Gen Z style"""
        risk_level = risk_analysis["risk_level"]
        risk_score = risk_analysis["risk_score"]
        volatility = risk_analysis["volatility"]
        
        if risk_level == "High":
            emoji = "🚨"
            status = "HIGH RISK ALERT! 🚨"
        elif risk_level == "Medium":
            emoji = "⚠️"
            status = "Medium Risk ⚠️"
        else:
            emoji = "✅"
            status = "Low Risk ✅"
        
        response = f"""
        {emoji} RISK ANALYSIS REPORT {emoji}
        
        📊 Risk Level: {status}
        🎯 Risk Score: {risk_score:.2%}
        📈 Volatility: {volatility:.2%}
        
        🔍 Key Findings:
        • Sector Concentration: {risk_analysis['sector_concentration']:.2%}
        • Country Concentration: {risk_analysis['country_concentration']:.2%}
        
        💡 Recommendations:
        """
        
        for rec in risk_analysis["recommendations"]:
            response += f"• {rec}\n"
        
        return response
    
    def _format_normal_risk_response(self, risk_analysis: Dict[str, Any]) -> str:
        """Format risk response in normal style"""
        risk_level = risk_analysis["risk_level"]
        risk_score = risk_analysis["risk_score"]
        
        response = f"""
        Portfolio Risk Analysis Report
        
        Risk Level: {risk_level}
        Risk Score: {risk_score:.2%}
        Volatility: {risk_analysis['volatility']:.2%}
        
        Key Risk Metrics:
        • Sector Concentration: {risk_analysis['sector_concentration']:.2%}
        • Country Concentration: {risk_analysis['country_concentration']:.2%}
        
        Recommendations:
        """
        
        for rec in risk_analysis["recommendations"]:
            response += f"• {rec}\n"
        
        return response

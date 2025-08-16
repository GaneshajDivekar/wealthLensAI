from typing import Dict, Any
from agents.base_agent import BaseAgent
from data.portfolio_data import get_portfolio_data
import random

class TechnicalAnalyzerAgent(BaseAgent):
    """Agent for technical analysis and chart pattern recognition"""
    
    def __init__(self):
        super().__init__(
            name="Technical Analyzer",
            description="Provides technical analysis and chart pattern insights"
        )
        
        # Technical indicators data (simulated)
        self.technical_patterns = {
            "Bullish": ["Ascending Triangle", "Cup and Handle", "Double Bottom", "Golden Cross"],
            "Bearish": ["Descending Triangle", "Head and Shoulders", "Double Top", "Death Cross"],
            "Neutral": ["Rectangle", "Pennant", "Flag", "Symmetrical Triangle"]
        }
        
        self.indicators = {
            "RSI": {"oversold": 30, "overbought": 70},
            "MACD": {"signal": "positive", "histogram": "increasing"},
            "Moving_Averages": {"sma_20": "above", "sma_50": "support"},
            "Bollinger_Bands": {"position": "middle", "width": "normal"}
        }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process technical analysis request"""
        query = input_data.get("query", "")
        user_language = input_data.get("language", "normal")
        
        try:
            # Get portfolio stocks for analysis
            portfolio_stocks = self._get_portfolio_stocks()
            
            # Perform technical analysis
            technical_analysis = self._perform_technical_analysis(portfolio_stocks)
            
            # Generate response based on language preference
            response = self._format_technical_response(technical_analysis, user_language)
            
            return {
                "agent": self.name,
                "response": response + "\n\n📈 Source: Technical Analyzer Agent",
                "data": technical_analysis,
                "type": "technical_analysis"
            }
            
        except Exception as e:
            print(f"Error in technical analyzer: {e}")
            return {
                "agent": self.name,
                "response": "Sorry, I couldn't perform technical analysis at the moment.",
                "data": {"error": str(e)},
                "type": "error"
            }
    
    def _get_portfolio_stocks(self) -> list:
        """Get stocks from portfolio for analysis"""
        portfolio_data = get_portfolio_data()
        return portfolio_data['stocks']
    
    def _perform_technical_analysis(self, stocks: list) -> Dict[str, Any]:
        """Perform technical analysis on portfolio stocks"""
        stock_analysis = {}
        
        for stock in stocks:
            stock_symbol = stock['symbol']
            
            # Generate technical indicators (simulated)
            rsi = random.uniform(20, 80)
            macd_signal = random.choice(["positive", "negative", "neutral"])
            moving_average_trend = random.choice(["bullish", "bearish", "neutral"])
            pattern = self._generate_chart_pattern()
            
            # Determine overall technical signal
            technical_signal = self._determine_technical_signal(rsi, macd_signal, moving_average_trend, pattern)
            
            stock_analysis[stock_symbol] = {
                "rsi": rsi,
                "macd_signal": macd_signal,
                "moving_average_trend": moving_average_trend,
                "chart_pattern": pattern,
                "technical_signal": technical_signal,
                "support_level": stock['current_price'] * random.uniform(0.85, 0.95),
                "resistance_level": stock['current_price'] * random.uniform(1.05, 1.15),
                "recommendations": self._generate_technical_recommendations(technical_signal, rsi, pattern)
            }
        
        # Overall technical analysis
        overall_analysis = self._generate_overall_technical_analysis(stock_analysis)
        
        return {
            "stock_analysis": stock_analysis,
            "overall_analysis": overall_analysis,
            "market_sentiment": self._get_market_sentiment(),
            "key_levels": self._get_key_levels(stock_analysis)
        }
    
    def _generate_chart_pattern(self) -> str:
        """Generate a random chart pattern"""
        pattern_type = random.choice(list(self.technical_patterns.keys()))
        pattern = random.choice(self.technical_patterns[pattern_type])
        return f"{pattern} ({pattern_type.lower()})"
    
    def _determine_technical_signal(self, rsi: float, macd: str, ma_trend: str, pattern: str) -> str:
        """Determine overall technical signal"""
        bullish_signals = 0
        bearish_signals = 0
        
        # RSI analysis
        if rsi < 30:
            bullish_signals += 1
        elif rsi > 70:
            bearish_signals += 1
        
        # MACD analysis
        if macd == "positive":
            bullish_signals += 1
        elif macd == "negative":
            bearish_signals += 1
        
        # Moving average analysis
        if ma_trend == "bullish":
            bullish_signals += 1
        elif ma_trend == "bearish":
            bearish_signals += 1
        
        # Pattern analysis
        if "Bullish" in pattern:
            bullish_signals += 1
        elif "Bearish" in pattern:
            bearish_signals += 1
        
        # Determine overall signal
        if bullish_signals > bearish_signals:
            return "Strong Buy" if bullish_signals >= 3 else "Buy"
        elif bearish_signals > bullish_signals:
            return "Strong Sell" if bearish_signals >= 3 else "Sell"
        else:
            return "Hold"
    
    def _generate_technical_recommendations(self, signal: str, rsi: float, pattern: str) -> list:
        """Generate technical recommendations"""
        recommendations = []
        
        if signal in ["Strong Buy", "Buy"]:
            recommendations.append("Consider adding to position")
            recommendations.append("Set stop-loss below support level")
        elif signal in ["Strong Sell", "Sell"]:
            recommendations.append("Consider reducing position")
            recommendations.append("Wait for better entry point")
        else:
            recommendations.append("Monitor for breakout/breakdown")
            recommendations.append("Maintain current position")
        
        # RSI-specific recommendations
        if rsi < 30:
            recommendations.append("RSI indicates oversold conditions - potential bounce")
        elif rsi > 70:
            recommendations.append("RSI indicates overbought conditions - potential pullback")
        
        # Pattern-specific recommendations
        if "Bullish" in pattern:
            recommendations.append("Chart pattern suggests upward momentum")
        elif "Bearish" in pattern:
            recommendations.append("Chart pattern suggests downward pressure")
        
        return recommendations
    
    def _generate_overall_technical_analysis(self, stock_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall technical analysis"""
        signals = [analysis["technical_signal"] for analysis in stock_analysis.values()]
        
        buy_signals = sum(1 for signal in signals if "Buy" in signal)
        sell_signals = sum(1 for signal in signals if "Sell" in signal)
        hold_signals = sum(1 for signal in signals if signal == "Hold")
        
        total_stocks = len(stock_analysis)
        
        if buy_signals / total_stocks > 0.5:
            overall_signal = "Bullish"
        elif sell_signals / total_stocks > 0.5:
            overall_signal = "Bearish"
        else:
            overall_signal = "Neutral"
        
        return {
            "overall_signal": overall_signal,
            "buy_signals": buy_signals,
            "sell_signals": sell_signals,
            "hold_signals": hold_signals,
            "total_stocks": total_stocks,
            "key_insights": [
                "Most stocks showing positive technical momentum",
                "Support levels holding across portfolio",
                "Volume patterns suggest institutional buying"
            ]
        }
    
    def _get_market_sentiment(self) -> Dict[str, Any]:
        """Get market sentiment indicators"""
        return {
            "fear_greed_index": random.randint(30, 70),
            "put_call_ratio": random.uniform(0.8, 1.2),
            "vix_level": random.uniform(15, 25),
            "advance_decline_ratio": random.uniform(0.8, 1.5)
        }
    
    def _get_key_levels(self, stock_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Get key support and resistance levels"""
        support_levels = []
        resistance_levels = []
        
        for symbol, analysis in stock_analysis.items():
            support_levels.append({
                "symbol": symbol,
                "level": analysis["support_level"],
                "strength": random.choice(["Strong", "Moderate", "Weak"])
            })
            
            resistance_levels.append({
                "symbol": symbol,
                "level": analysis["resistance_level"],
                "strength": random.choice(["Strong", "Moderate", "Weak"])
            })
        
        return {
            "support_levels": support_levels,
            "resistance_levels": resistance_levels
        }
    
    def _format_technical_response(self, technical_analysis: Dict[str, Any], language: str) -> str:
        """Format technical analysis response based on language preference"""
        if language == "genz":
            return self._format_genz_technical_response(technical_analysis)
        else:
            return self._format_normal_technical_response(technical_analysis)
    
    def _format_genz_technical_response(self, technical_analysis: Dict[str, Any]) -> str:
        """Format technical response in Gen Z style"""
        overall = technical_analysis["overall_analysis"]
        
        if overall["overall_signal"] == "Bullish":
            emoji = "🚀"
            status = "BULLISH MOMENTUM! 🚀"
        elif overall["overall_signal"] == "Bearish":
            emoji = "📉"
            status = "BEARISH PRESSURE 📉"
        else:
            emoji = "📊"
            status = "NEUTRAL ZONE 📊"
        
        response = f"""
        📈 TECHNICAL ANALYSIS REPORT 📈
        
        {emoji} Overall Signal: {status}
        🎯 Buy Signals: {overall['buy_signals']}/{overall['total_stocks']}
        ⚠️ Sell Signals: {overall['sell_signals']}/{overall['total_stocks']}
        📊 Hold Signals: {overall['hold_signals']}/{overall['total_stocks']}
        
        🔥 TOP TECHNICAL PICKS:
        """
        
        # Show top 3 stocks with strongest signals
        stock_signals = []
        for symbol, analysis in technical_analysis["stock_analysis"].items():
            signal_strength = 0
            if "Strong Buy" in analysis["technical_signal"]:
                signal_strength = 3
            elif "Buy" in analysis["technical_signal"]:
                signal_strength = 2
            elif "Hold" in analysis["technical_signal"]:
                signal_strength = 1
            
            stock_signals.append((symbol, signal_strength, analysis))
        
        stock_signals.sort(key=lambda x: x[1], reverse=True)
        
        for i, (symbol, strength, analysis) in enumerate(stock_signals[:3]):
            emoji = "🚀" if strength >= 2 else "📊"
            response += f"{emoji} {symbol}: {analysis['technical_signal']}\n"
            response += f"   RSI: {analysis['rsi']:.1f} | Pattern: {analysis['chart_pattern']}\n"
        
        response += "\n💡 KEY INSIGHTS:\n"
        for insight in overall["key_insights"]:
            response += f"• {insight}\n"
        
        return response
    
    def _format_normal_technical_response(self, technical_analysis: Dict[str, Any]) -> str:
        """Format technical response in normal style"""
        overall = technical_analysis["overall_analysis"]
        
        response = f"""
        Technical Analysis Report
        
        Overall Signal: {overall['overall_signal']}
        Buy Signals: {overall['buy_signals']}/{overall['total_stocks']}
        Sell Signals: {overall['sell_signals']}/{overall['total_stocks']}
        Hold Signals: {overall['hold_signals']}/{overall['total_stocks']}
        
        Top Technical Picks:
        """
        
        # Show top 3 stocks with strongest signals
        stock_signals = []
        for symbol, analysis in technical_analysis["stock_analysis"].items():
            signal_strength = 0
            if "Strong Buy" in analysis["technical_signal"]:
                signal_strength = 3
            elif "Buy" in analysis["technical_signal"]:
                signal_strength = 2
            elif "Hold" in analysis["technical_signal"]:
                signal_strength = 1
            
            stock_signals.append((symbol, signal_strength, analysis))
        
        stock_signals.sort(key=lambda x: x[1], reverse=True)
        
        for i, (symbol, strength, analysis) in enumerate(stock_signals[:3]):
            response += f"{i+1}. {symbol}: {analysis['technical_signal']}\n"
            response += f"   RSI: {analysis['rsi']:.1f} | Pattern: {analysis['chart_pattern']}\n"
            response += f"   Support: ₹{analysis['support_level']:.2f} | Resistance: ₹{analysis['resistance_level']:.2f}\n"
        
        response += "\nKey Insights:\n"
        for insight in overall["key_insights"]:
            response += f"• {insight}\n"
        
        return response

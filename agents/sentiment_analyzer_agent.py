from typing import Dict, Any
from agents.base_agent import BaseAgent
from data.portfolio_data import get_portfolio_data
import random

class SentimentAnalyzerAgent(BaseAgent):
    """Agent for analyzing market sentiment and investor psychology"""
    
    def __init__(self):
        super().__init__(
            name="Sentiment Analyzer",
            description="Analyzes market sentiment and investor psychology"
        )
        
        # Sentiment data (simulated)
        self.sentiment_indicators = {
            "social_media": {
                "twitter_sentiment": "positive",
                "reddit_sentiment": "neutral",
                "stocktwits_sentiment": "positive"
            },
            "news_sentiment": {
                "headlines": "positive",
                "earnings_news": "positive",
                "analyst_ratings": "bullish"
            },
            "institutional": {
                "insider_buying": "increasing",
                "institutional_flows": "positive",
                "hedge_fund_activity": "active"
            }
        }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process sentiment analysis request"""
        query = input_data.get("query", "")
        user_language = input_data.get("language", "normal")
        
        try:
            # Get portfolio stocks for sentiment analysis
            portfolio_stocks = self._get_portfolio_stocks()
            
            # Perform sentiment analysis
            sentiment_analysis = self._perform_sentiment_analysis(portfolio_stocks)
            
            # Generate response based on language preference
            response = self._format_sentiment_response(sentiment_analysis, user_language)
            
            return {
                "agent": self.name,
                "response": response + "\n\n😎 Source: Sentiment Analyzer Agent",
                "data": sentiment_analysis,
                "type": "sentiment_analysis"
            }
            
        except Exception as e:
            print(f"Error in sentiment analyzer: {e}")
            return {
                "agent": self.name,
                "response": "Sorry, I couldn't analyze sentiment at the moment.",
                "data": {"error": str(e)},
                "type": "error"
            }
    
    def _get_portfolio_stocks(self) -> list:
        """Get stocks from portfolio for sentiment analysis"""
        portfolio_data = get_portfolio_data()
        return portfolio_data['stocks']
    
    def _perform_sentiment_analysis(self, stocks: list) -> Dict[str, Any]:
        """Perform sentiment analysis on portfolio stocks"""
        stock_sentiment = {}
        
        for stock in stocks:
            stock_symbol = stock['symbol']
            
            # Generate sentiment scores (simulated)
            social_sentiment = random.uniform(-1, 1)  # -1 to 1 scale
            news_sentiment = random.uniform(-1, 1)
            institutional_sentiment = random.uniform(-1, 1)
            
            # Calculate overall sentiment
            overall_sentiment = (social_sentiment + news_sentiment + institutional_sentiment) / 3
            
            # Determine sentiment category
            sentiment_category = self._categorize_sentiment(overall_sentiment)
            
            stock_sentiment[stock_symbol] = {
                "social_sentiment": social_sentiment,
                "news_sentiment": news_sentiment,
                "institutional_sentiment": institutional_sentiment,
                "overall_sentiment": overall_sentiment,
                "sentiment_category": sentiment_category,
                "sentiment_score": self._convert_to_score(overall_sentiment),
                "trend": self._get_sentiment_trend(),
                "key_drivers": self._get_sentiment_drivers(sentiment_category),
                "recommendations": self._generate_sentiment_recommendations(sentiment_category, overall_sentiment)
            }
        
        # Overall sentiment analysis
        overall_analysis = self._generate_overall_sentiment_analysis(stock_sentiment)
        
        return {
            "stock_sentiment": stock_sentiment,
            "overall_analysis": overall_analysis,
            "market_sentiment": self._get_market_sentiment(),
            "sentiment_indicators": self.sentiment_indicators
        }
    
    def _categorize_sentiment(self, sentiment_score: float) -> str:
        """Categorize sentiment based on score"""
        if sentiment_score > 0.5:
            return "Very Bullish"
        elif sentiment_score > 0.2:
            return "Bullish"
        elif sentiment_score > -0.2:
            return "Neutral"
        elif sentiment_score > -0.5:
            return "Bearish"
        else:
            return "Very Bearish"
    
    def _convert_to_score(self, sentiment: float) -> int:
        """Convert sentiment to 0-100 score"""
        return int((sentiment + 1) * 50)
    
    def _get_sentiment_trend(self) -> str:
        """Get sentiment trend"""
        return random.choice(["Improving", "Stable", "Declining"])
    
    def _get_sentiment_drivers(self, category: str) -> list:
        """Get key drivers for sentiment category"""
        if "Bullish" in category:
            return [
                "Positive earnings reports",
                "Strong analyst recommendations",
                "Institutional buying activity",
                "Positive social media buzz"
            ]
        elif "Bearish" in category:
            return [
                "Negative news coverage",
                "Analyst downgrades",
                "Institutional selling",
                "Negative social media sentiment"
            ]
        else:
            return [
                "Mixed analyst opinions",
                "Neutral news coverage",
                "Balanced institutional activity",
                "Mixed social media sentiment"
            ]
    
    def _generate_sentiment_recommendations(self, category: str, sentiment_score: float) -> list:
        """Generate recommendations based on sentiment"""
        recommendations = []
        
        if "Very Bullish" in category:
            recommendations.append("Consider increasing position size")
            recommendations.append("Monitor for potential overvaluation")
            recommendations.append("Set trailing stop-loss to protect gains")
        elif "Bullish" in category:
            recommendations.append("Hold current position")
            recommendations.append("Consider adding on dips")
            recommendations.append("Monitor sentiment for changes")
        elif "Neutral" in category:
            recommendations.append("Maintain current position")
            recommendations.append("Wait for clearer sentiment signals")
            recommendations.append("Focus on fundamental analysis")
        elif "Bearish" in category:
            recommendations.append("Consider reducing position")
            recommendations.append("Wait for sentiment improvement")
            recommendations.append("Set tight stop-loss")
        else:  # Very Bearish
            recommendations.append("Consider exiting position")
            recommendations.append("Wait for sentiment reversal")
            recommendations.append("Look for contrarian opportunities")
        
        return recommendations
    
    def _generate_overall_sentiment_analysis(self, stock_sentiment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall sentiment analysis"""
        sentiments = [analysis["overall_sentiment"] for analysis in stock_sentiment.values()]
        categories = [analysis["sentiment_category"] for analysis in stock_sentiment.values()]
        
        avg_sentiment = sum(sentiments) / len(sentiments)
        
        bullish_count = sum(1 for cat in categories if "Bullish" in cat)
        bearish_count = sum(1 for cat in categories if "Bearish" in cat)
        neutral_count = len(categories) - bullish_count - bearish_count
        
        total_stocks = len(stock_sentiment)
        
        if bullish_count / total_stocks > 0.5:
            overall_sentiment = "Bullish"
        elif bearish_count / total_stocks > 0.5:
            overall_sentiment = "Bearish"
        else:
            overall_sentiment = "Neutral"
        
        return {
            "overall_sentiment": overall_sentiment,
            "average_sentiment_score": avg_sentiment,
            "bullish_stocks": bullish_count,
            "bearish_stocks": bearish_count,
            "neutral_stocks": neutral_count,
            "total_stocks": total_stocks,
            "sentiment_distribution": {
                "very_bullish": sum(1 for cat in categories if cat == "Very Bullish"),
                "bullish": sum(1 for cat in categories if cat == "Bullish"),
                "neutral": sum(1 for cat in categories if cat == "Neutral"),
                "bearish": sum(1 for cat in categories if cat == "Bearish"),
                "very_bearish": sum(1 for cat in categories if cat == "Very Bearish")
            },
            "key_insights": [
                "Social media sentiment trending positive",
                "Institutional flows showing confidence",
                "News sentiment generally favorable"
            ]
        }
    
    def _get_market_sentiment(self) -> Dict[str, Any]:
        """Get overall market sentiment indicators"""
        return {
            "fear_greed_index": random.randint(40, 80),
            "put_call_ratio": random.uniform(0.7, 1.1),
            "vix_level": random.uniform(12, 22),
            "advance_decline_ratio": random.uniform(1.0, 1.8),
            "bull_bear_ratio": random.uniform(1.2, 2.0),
            "insider_buying_ratio": random.uniform(0.8, 1.5)
        }
    
    def _format_sentiment_response(self, sentiment_analysis: Dict[str, Any], language: str) -> str:
        """Format sentiment analysis response based on language preference"""
        if language == "genz":
            return self._format_genz_sentiment_response(sentiment_analysis)
        else:
            return self._format_normal_sentiment_response(sentiment_analysis)
    
    def _format_genz_sentiment_response(self, sentiment_analysis: Dict[str, Any]) -> str:
        """Format sentiment response in Gen Z style"""
        overall = sentiment_analysis["overall_analysis"]
        
        if overall["overall_sentiment"] == "Bullish":
            emoji = "🚀"
            status = "BULLISH VIBES! 🚀"
        elif overall["overall_sentiment"] == "Bearish":
            emoji = "😰"
            status = "BEARISH MOOD 😰"
        else:
            emoji = "😐"
            status = "NEUTRAL VIBES 😐"
        
        response = f"""
        😎 SENTIMENT ANALYSIS REPORT 😎
        
        {emoji} Overall Mood: {status}
        📊 Average Sentiment: {overall['average_sentiment_score']:.2f}
        🚀 Bullish Stocks: {overall['bullish_stocks']}/{overall['total_stocks']}
        😰 Bearish Stocks: {overall['bearish_stocks']}/{overall['total_stocks']}
        
        🔥 TOP SENTIMENT PICKS:
        """
        
        # Show top 3 stocks with best sentiment
        stock_sentiments = []
        for symbol, analysis in sentiment_analysis["stock_sentiment"].items():
            stock_sentiments.append((symbol, analysis["overall_sentiment"], analysis))
        
        stock_sentiments.sort(key=lambda x: x[1], reverse=True)
        
        for i, (symbol, sentiment, analysis) in enumerate(stock_sentiments[:3]):
            if sentiment > 0.5:
                emoji = "🚀"
            elif sentiment > 0:
                emoji = "📈"
            elif sentiment > -0.5:
                emoji = "📊"
            else:
                emoji = "📉"
            
            response += f"{emoji} {symbol}: {analysis['sentiment_category']}\n"
            response += f"   Score: {analysis['sentiment_score']}/100 | Trend: {analysis['trend']}\n"
        
        response += "\n💡 KEY INSIGHTS:\n"
        for insight in overall["key_insights"]:
            response += f"• {insight}\n"
        
        response += "\n📱 SOCIAL SENTIMENT:\n"
        social = sentiment_analysis["sentiment_indicators"]["social_media"]
        response += f"• Twitter: {social['twitter_sentiment'].title()} 📱\n"
        response += f"• Reddit: {social['reddit_sentiment'].title()} 🤖\n"
        response += f"• StockTwits: {social['stocktwits_sentiment'].title()} 💬\n"
        
        return response
    
    def _format_normal_sentiment_response(self, sentiment_analysis: Dict[str, Any]) -> str:
        """Format sentiment response in normal style"""
        overall = sentiment_analysis["overall_analysis"]
        
        response = f"""
        Market Sentiment Analysis Report
        
        Overall Sentiment: {overall['overall_sentiment']}
        Average Sentiment Score: {overall['average_sentiment_score']:.2f}
        Bullish Stocks: {overall['bullish_stocks']}/{overall['total_stocks']}
        Bearish Stocks: {overall['bearish_stocks']}/{overall['total_stocks']}
        Neutral Stocks: {overall['neutral_stocks']}/{overall['total_stocks']}
        
        Top Sentiment Picks:
        """
        
        # Show top 3 stocks with best sentiment
        stock_sentiments = []
        for symbol, analysis in sentiment_analysis["stock_sentiment"].items():
            stock_sentiments.append((symbol, analysis["overall_sentiment"], analysis))
        
        stock_sentiments.sort(key=lambda x: x[1], reverse=True)
        
        for i, (symbol, sentiment, analysis) in enumerate(stock_sentiments[:3]):
            response += f"{i+1}. {symbol}: {analysis['sentiment_category']}\n"
            response += f"   Sentiment Score: {analysis['sentiment_score']}/100\n"
            response += f"   Trend: {analysis['trend']}\n"
            response += f"   Key Drivers: {', '.join(analysis['key_drivers'][:2])}\n"
        
        response += "\nKey Insights:\n"
        for insight in overall["key_insights"]:
            response += f"• {insight}\n"
        
        response += "\nSentiment Distribution:\n"
        dist = overall["sentiment_distribution"]
        response += f"• Very Bullish: {dist['very_bullish']}\n"
        response += f"• Bullish: {dist['bullish']}\n"
        response += f"• Neutral: {dist['neutral']}\n"
        response += f"• Bearish: {dist['bearish']}\n"
        response += f"• Very Bearish: {dist['very_bearish']}\n"
        
        return response

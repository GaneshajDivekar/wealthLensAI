from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from agents.portfolio_analyzer_agent import PortfolioAnalyzerAgent
from agents.news_analyzer_agent import NewsAnalyzerAgent
from agents.investment_advisor_agent import InvestmentAdvisorAgent
from agents.rag_agent import RAGAgent
from agents.risk_analyzer_agent import RiskAnalyzerAgent
from agents.market_research_agent import MarketResearchAgent
from agents.technical_analyzer_agent import TechnicalAnalyzerAgent
from agents.sentiment_analyzer_agent import SentimentAnalyzerAgent
import json

class MasterAgent(BaseAgent):
    """Master agent that handles intent classification and routes requests to appropriate agents"""
    
    def __init__(self):
        super().__init__(
            name="Master Agent",
            description="Orchestrates all agents and handles intent classification"
        )
        
        # Initialize all specialized agents
        self.agents = {
            "portfolio_analyzer": PortfolioAnalyzerAgent(),
            "news_analyzer": NewsAnalyzerAgent(),
            "investment_advisor": InvestmentAdvisorAgent(),
            "rag_agent": RAGAgent(),
            "risk_analyzer": RiskAnalyzerAgent(),
            "market_research": MarketResearchAgent(),
            "technical_analyzer": TechnicalAnalyzerAgent(),
            "sentiment_analyzer": SentimentAnalyzerAgent()
        }
        
        # Intent classification patterns
        self.intent_patterns = {
            "portfolio_analysis": [
                # Portfolio related
                "portfolio", "performance", "returns", "value", "summary",
                "penny stocks", "sector", "country", "risk", "volatility",
                "holdings", "assets", "investment", "stocks", "funds",
                # Price related
                "price", "current price", "stock price", "share price", "market price",
                "what is the price", "how much is", "current value", "market value",
                # Variations and synonyms
                "my portfolio", "portfolio status", "portfolio value", "portfolio summary",
                "show portfolio", "portfolio overview", "portfolio performance",
                "my stocks", "my investments", "investment summary", "stock summary",
                "portfolio breakdown", "portfolio analysis", "portfolio report",
                "show me my portfolio", "what is my portfolio", "portfolio details",
                "price of", "current price of", "stock price of", "share price of",
                "what is the current price", "how much is the price", "price for",
                # Common misspellings
                "portfolo", "portfollio", "portfoli", "perfomance", "retrns", "val",
                "summry", "peny stocks", "sctr", "cntry", "rsk", "volatilty",
                "holdngs", "assest", "investmnt", "stoks", "fnds", "prce", "currnt prce"
            ],
            "news_analysis": [
                # News related
                "news", "market", "traffic", "impact", "events", "geopolitical",
                "headlines", "latest", "breaking", "announcement", "update",
                # Variations and synonyms
                "how news", "news impact", "market news", "latest news", "current news",
                "news analysis", "news affect", "news influence", "market events",
                "current events", "latest developments", "market developments",
                "how does news", "news effect", "news impact on", "market impact",
                "traffic issues", "traffic problems", "traffic affect", "traffic impact",
                "how does traffic", "traffic between", "traffic affect stocks",
                # Common misspellings
                "nws", "mrket", "trffic", "impct", "evnts", "geopolitcal", "hedlines",
                "ltest", "brking", "announcemnt", "updte"
            ],
            "investment_advice": [
                # Investment related
                "buy", "sell", "hold", "recommendation", "advice", "invest",
                "opportunity", "strategy", "should i", "what to", "where to",
                # Variations and synonyms
                "what should i buy", "what should i sell", "what should i hold",
                "buy recommendations", "sell recommendations", "hold recommendations",
                "investment advice", "investment suggestions", "investment recommendations",
                "what to buy", "what to sell", "what to hold", "buying advice",
                "selling advice", "holding advice", "investment opportunities",
                "should i buy", "should i sell", "should i hold", "recommendations",
                "give me advice", "investment tips", "buying tips", "selling tips",
                # Common misspellings
                "by", "sel", "hol", "recomendatn", "advise", "invest", "opportnity",
                "stratgy", "shuld i", "wat to", "wher to"
            ],
            "personal_info": [
                # Personal info related
                "who", "ganesh", "contact", "work", "experience", "expertise",
                "background", "company", "role", "about", "tell me about", "who am i",
                # Variations and synonyms
                "who is ganesh", "ganesh divekar", "ganesh contact", "ganesh phone",
                "ganesh number", "ganesh company", "ganesh work", "ganesh role",
                "about ganesh", "ganesh position", "ganesh information", "ganesh details",
                "tell me about ganesh", "ganesh background", "ganesh profile",
                "ganesh contact number", "ganesh phone number", "ganesh work details",
                "who am i", "my information", "my details", "my profile", "my background",
                "tell me about myself", "my contact", "my work", "my experience",
                "what is my name", "my name", "about me", "tell me about me",
                "who am i", "what is my", "my personal", "my info", "my data",
                # Common misspellings
                "ganesh", "ganes", "ganesh", "contct", "wrk", "experince", "expertse",
                "backgrnd", "compny", "rol", "abt", "tel me abt", "who am i", "who am i"
            ],
            "risk_assessment": [
                # Risk related
                "risk", "danger", "safe", "volatile", "stability", "security",
                "protection", "hedge", "diversification", "exposure", "risk level",
                "risk assessment", "portfolio risk", "volatility", "safety",
                # Variations and synonyms
                "risk analysis", "risk level", "risk assessment", "portfolio risk",
                "how risky", "risk evaluation", "risk measurement", "risk profile",
                "risk status", "risk overview", "risk summary", "risk report",
                "volatility analysis", "safety assessment", "security analysis",
                "danger level", "stability analysis", "exposure analysis",
                "how safe", "is my portfolio safe", "portfolio safety", "risk check",
                # Common misspellings
                "rsk", "dnger", "sfe", "volatle", "stablty", "securty", "protctn",
                "hedg", "diversifcatn", "exposre", "volatilty", "saftey"
            ],
            "market_research": [
                # Market research related
                "research", "analysis", "study", "trends", "market", "industry",
                "competition", "growth", "potential", "outlook", "forecast",
                # Variations and synonyms
                "market research", "market analysis", "market trends", "market study",
                "market outlook", "market forecast", "market prediction", "market growth",
                "sector analysis", "industry analysis", "industry trends", "industry research",
                "market insights", "market intelligence", "market data", "market information",
                "sector research", "sector trends", "sector outlook", "sector forecast",
                "market study", "industry study", "sector study", "market trends analysis",
                # Common misspellings
                "reserch", "anlysis", "stdy", "trnds", "mrket", "indstry", "competitn",
                "grwth", "potentil", "outlok", "forcast"
            ],
            "technical_analysis": [
                # Technical analysis related
                "technical", "chart", "pattern", "indicator", "moving average",
                "rsi", "macd", "support", "resistance", "breakout", "trend",
                # Variations and synonyms
                "technical analysis", "chart analysis", "pattern analysis", "technical indicators",
                "chart patterns", "technical signals", "technical trends", "technical momentum",
                "rsi analysis", "macd analysis", "support levels", "resistance levels",
                "trend analysis", "momentum analysis", "signal analysis", "technical study",
                "chart study", "pattern study", "indicator analysis", "technical evaluation",
                "technical charts", "chart patterns", "technical signals", "technical indicators",
                # Common misspellings
                "techncal", "chrt", "patern", "indictor", "movng avrage", "rs", "mac",
                "suport", "resistance", "breakot", "trnd"
            ],
            "sentiment_analysis": [
                # Sentiment related
                "sentiment", "mood", "feeling", "opinion", "perception", "confidence",
                "fear", "greed", "bullish", "bearish", "market sentiment",
                # Variations and synonyms
                "sentiment analysis", "market sentiment", "investor sentiment", "social sentiment",
                "media sentiment", "public sentiment", "market mood", "investor mood",
                "market feeling", "market emotion", "market psychology", "social media sentiment",
                "public opinion", "market perception", "investor confidence", "market fear",
                "sentiment study", "mood analysis", "feeling analysis", "emotion analysis",
                "market mood analysis", "investor mood analysis", "market psychology analysis",
                # Common misspellings
                "sentimnt", "md", "feeling", "opnion", "perceptn", "confdence", "fr",
                "gred", "bullsh", "bearsh", "mrket sentimnt"
            ]
        }
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process query with intent classification and routing"""
        query = input_data.get("query", "")
        user_language = input_data.get("language", "normal")
        
        try:
            # Step 1: Intent Classification
            intent = self._classify_intent(query)
            
            # Step 2: Route to appropriate agent(s)
            agent_responses = self._route_to_agents(query, intent, user_language)
            
            # Step 3: Generate final response
            final_response = self._generate_final_response(agent_responses, user_language)
            
            return {
                "agent": self.name,
                "response": final_response,
                "data": {
                    "query": query,
                    "intent": intent,
                    "agent_responses": agent_responses,
                    "routing_info": {
                        "primary_intent": intent["primary"],
                        "confidence": intent["confidence"],
                        "agents_used": list(agent_responses.keys())
                    }
                },
                "type": "master_response"
            }
            
        except Exception as e:
            print(f"Error in master agent: {e}")
            return {
                "agent": self.name,
                "response": "I'm sorry, I encountered an error processing your request. Please try again.",
                "data": {"error": str(e)},
                "type": "error"
            }
    
    def _classify_intent(self, query: str) -> Dict[str, Any]:
        """Classify the intent of the user query with flexible matching"""
        query_lower = query.lower()
        
        # Special case for "who am i" - more comprehensive check
        if (query_lower.strip() == "who am i" or 
            query_lower.strip() == "who am i?" or
            query_lower.strip() == "who am i." or
            query_lower.strip() == "whoami" or
            query_lower.strip() == "who am i "):
            print(f"DEBUG: Special case triggered for query: '{query}'")
            return {
                "primary": "personal_info",
                "confidence": 1.0,
                "secondary": [],
                "all_scores": {"personal_info": 1.0}
            }
        
        # Special case for price queries
        if ("price" in query_lower and ("current" in query_lower or "what is" in query_lower or "how much" in query_lower)):
            print(f"DEBUG: Price query special case triggered for query: '{query}'")
            return {
                "primary": "portfolio_analysis",
                "confidence": 1.0,
                "secondary": [],
                "all_scores": {"portfolio_analysis": 1.0}
            }
        
        # Clean and normalize query
        import re
        query_clean = re.sub(r'[^\w\s]', ' ', query_lower)
        query_words = query_clean.split()
        
        # Calculate confidence scores for each intent
        intent_scores = {}
        
        for intent_name, patterns in self.intent_patterns.items():
            score = 0
            total_patterns = len(patterns)
            
            for pattern in patterns:
                # Exact match (highest score)
                if pattern == query_lower.strip():
                    score += 2.0
                elif pattern in query_lower:
                    score += 1.0
                # Partial word match (medium score)
                elif any(word in pattern for word in query_words):
                    score += 0.7
                # Word similarity (lower score for typos)
                elif self._word_similarity(pattern, query_words):
                    score += 0.5
            
            # Normalize score
            intent_scores[intent_name] = score / total_patterns if total_patterns > 0 else 0
        
        # Find primary intent
        primary_intent = max(intent_scores.items(), key=lambda x: x[1])
        
        # Get secondary intents (if any have significant scores)
        secondary_intents = [
            intent for intent, score in intent_scores.items() 
            if score > 0.1 and intent != primary_intent[0]
        ]
        
        return {
            "primary": primary_intent[0],
            "confidence": primary_intent[1],
            "secondary": secondary_intents,
            "all_scores": intent_scores
        }
    
    def _word_similarity(self, pattern: str, query_words: list) -> bool:
        """Check for word similarity to handle typos and variations"""
        for word in query_words:
            if len(word) >= 3 and len(pattern) >= 3:
                # Check if words are similar (handle common typos)
                if word in pattern or pattern in word:
                    return True
                # Check for common letter swaps and typos
                if len(word) == len(pattern):
                    diff_count = sum(1 for a, b in zip(word, pattern) if a != b)
                    if diff_count <= 2:  # Allow 2 character differences
                        return True
                # Check for common misspellings
                if self._is_common_misspelling(word, pattern):
                    return True
        return False
    
    def _is_common_misspelling(self, word: str, pattern: str) -> bool:
        """Check for common misspellings"""
        common_misspellings = {
            "portfolio": ["portfolo", "portfollio", "portfoli"],
            "performance": ["perfomance", "perfrmance"],
            "summary": ["summry", "sumary"],
            "news": ["nws", "newz"],
            "market": ["mrket", "markt"],
            "traffic": ["trffic", "trafik"],
            "impact": ["impct", "impackt"],
            "analysis": ["anlysis", "analisis"],
            "research": ["reserch", "recherch"],
            "technical": ["techncal", "techical"],
            "sentiment": ["sentimnt", "sentiment"],
            "investment": ["investmnt", "invesment"],
            "recommendation": ["recomendatn", "recomendation"],
            "ganesh": ["ganes", "ganesh"],
            "contact": ["contct", "contakt"],
            "risk": ["rsk", "risc"],
            "volatility": ["volatilty", "volatality"],
            "safety": ["saftey", "safte"],
            "trends": ["trnds", "trend"],
            "industry": ["indstry", "industy"]
        }
        
        if pattern in common_misspellings:
            return word in common_misspellings[pattern]
        return False
    
    def _route_to_agents(self, query: str, intent: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Route query to appropriate agents based on intent"""
        agent_responses = {}
        
        # Always route to primary intent agent
        primary_agent = self._get_agent_for_intent(intent["primary"])
        if primary_agent:
            try:
                response = primary_agent.process({
                    "query": query,
                    "language": language
                })
                agent_responses[intent["primary"]] = response
            except Exception as e:
                print(f"Error in {intent['primary']} agent: {e}")
                agent_responses[intent["primary"]] = {
                    "agent": intent["primary"].replace("_", " ").title(),
                    "response": "Sorry, I couldn't process this request.",
                    "type": "error"
                }
        
        # Route to secondary agents if confidence is high
        for secondary_intent in intent["secondary"]:
            if intent["all_scores"][secondary_intent] > 0.3:
                secondary_agent = self._get_agent_for_intent(secondary_intent)
                if secondary_agent:
                    try:
                        response = secondary_agent.process({
                            "query": query,
                            "language": language
                        })
                        agent_responses[secondary_intent] = response
                    except Exception as e:
                        print(f"Error in {secondary_intent} agent: {e}")
        
        # If no specific intent detected, use fallback
        if not agent_responses:
            fallback_agent = self.agents["rag_agent"]
            try:
                response = fallback_agent.process({
                    "query": query,
                    "language": language
                })
                agent_responses["fallback"] = response
            except Exception as e:
                print(f"Error in fallback agent: {e}")
        
        return agent_responses
    
    def _get_agent_for_intent(self, intent: str) -> BaseAgent:
        """Get the appropriate agent for a given intent"""
        agent_mapping = {
            "portfolio_analysis": self.agents["portfolio_analyzer"],
            "news_analysis": self.agents["news_analyzer"],
            "investment_advice": self.agents["investment_advisor"],
            "personal_info": self.agents["rag_agent"],
            "risk_assessment": self.agents["risk_analyzer"],
            "market_research": self.agents["market_research"],
            "technical_analysis": self.agents["technical_analyzer"],
            "sentiment_analysis": self.agents["sentiment_analyzer"]
        }
        
        return agent_mapping.get(intent)
    
    def _generate_final_response(self, agent_responses: Dict[str, Any], language: str) -> str:
        """Generate final response combining all agent outputs"""
        if not agent_responses:
            return "I'm sorry, I couldn't process your request. Please try again."
        
        if len(agent_responses) == 1:
            # Single agent response
            return list(agent_responses.values())[0]["response"]
        else:
            # Multiple agent responses - combine them
            return self._combine_responses(agent_responses, language)
    
    def _combine_responses(self, agent_responses: Dict[str, Any], language: str) -> str:
        """Combine multiple agent responses into a coherent response"""
        if language == "genz":
            combined = "🤖 Multi-Agent Analysis Complete! 🤖\n\n"
            
            for agent_name, response in agent_responses.items():
                agent_display_name = agent_name.replace("_", " ").title()
                agent_response = response.get("response", "")
                agent_type = response.get("type", "analysis")
                
                # Add source attribution
                source_emoji = self._get_source_emoji(agent_type)
                combined += f"{source_emoji} {agent_display_name} ({agent_type.replace('_', ' ').title()}):\n{agent_response}\n"
                
                if agent_name != list(agent_responses.keys())[-1]:
                    combined += "─" * 50 + "\n"
        else:
            combined = "Multi-Agent Analysis Complete!\n\n"
            
            for agent_name, response in agent_responses.items():
                agent_display_name = agent_name.replace("_", " ").title()
                agent_response = response.get("response", "")
                agent_type = response.get("type", "analysis")
                
                # Add source attribution
                combined += f"[{agent_display_name} - {agent_type.replace('_', ' ').title()}]\n{agent_response}\n"
                
                if agent_name != list(agent_responses.keys())[-1]:
                    combined += "-" * 50 + "\n"
        
        return combined
    
    def _get_source_emoji(self, agent_type: str) -> str:
        """Get appropriate emoji for agent type"""
        emoji_map = {
            "portfolio_summary": "📊",
            "portfolio_analysis": "📈",
            "risk_analysis": "⚠️",
            "news_analysis": "📰",
            "investment_advice": "💡",
            "buy_recommendations": "🛒",
            "sell_recommendations": "📉",
            "hold_recommendations": "⏸️",
            "rag_response": "👤",
            "market_research": "🔍",
            "technical_analysis": "📈",
            "sentiment_analysis": "😎",
            "error": "❌"
        }
        return emoji_map.get(agent_type, "📊")
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        status = {}
        for agent_name, agent in self.agents.items():
            try:
                status[agent_name] = agent.get_status()
            except Exception as e:
                status[agent_name] = {
                    "name": agent_name,
                    "status": "error",
                    "error": str(e)
                }
        return status
    
    def get_intent_analysis(self, query: str) -> Dict[str, Any]:
        """Get detailed intent analysis for a query"""
        intent = self._classify_intent(query)
        return {
            "query": query,
            "intent_analysis": intent,
            "available_intents": list(self.intent_patterns.keys()),
            "agent_mapping": {
                "portfolio_analysis": "Portfolio Analyzer",
                "news_analysis": "News Analyzer", 
                "investment_advice": "Investment Advisor",
                "personal_info": "RAG Agent",
                "risk_assessment": "Risk Analyzer",
                "market_research": "Market Research",
                "technical_analysis": "Technical Analyzer",
                "sentiment_analysis": "Sentiment Analyzer"
            }
        }

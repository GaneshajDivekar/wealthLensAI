from typing import Dict, Any, List, Optional
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
import re

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
        
        # Enhanced intent classification patterns with fuzzy matching support
        self.intent_patterns = {
            "portfolio_analysis": [
                # Portfolio related - Standard
                "portfolio", "performance", "returns", "value", "summary", "holdings", "assets", 
                "investment", "stocks", "funds", "penny stocks", "sector", "country", "volatility",
                # Price related - Standard
                "price", "current price", "stock price", "share price", "market price", "current value", "market value",
                # Gen Z Language
                "my bag", "my stonks", "my gains", "my losses", "stonk price", "diamond hands", "paper hands",
                "to the moon", "hodl", "my coins", "my plays", "my positions", "my picks", "fire stocks",
                "lit portfolio", "my investments slap", "portfolio hits different", "my money moves",
                "check my bag", "bag status", "portfolio vibes", "money printer", "tendies",
                # Casual/Slang variations
                "show my stuff", "what i got", "my money", "my cash", "how am i doing", "am i winning",
                "check my numbers", "my stats", "my progress", "whats good", "how we looking",
                "show me the money", "money talk", "cash money", "my dough", "my bread",
                # Question variations
                "what is the price", "how much is", "what does it cost", "whats the value",
                "how much worth", "what am i worth", "portfolio worth", "total value",
                "show me my portfolio", "what is my portfolio", "portfolio details", "portfolio status",
                "can you help me", "help me with", "i need help", "assist me", "support me",
                "can you analyze", "analyze my", "check my", "review my", "examine my",
                "portfolio analysis", "analyze portfolio", "portfolio review", "portfolio check",
                "my portfolio analysis", "portfolio breakdown", "portfolio overview", "portfolio summary",
                # Enlist queries
                "enlist stocks", "list stocks", "show stocks", "all stocks", "my stocks", "stock list",
                "enlist sectors", "list sectors", "show sectors", "all sectors", "sector list", "sectors in portfolio",
                "enlist countries", "list countries", "show countries", "all countries", "country list", "geographic breakdown",
                # Fuzzy/Typo variations
                "portfolo", "portfollio", "portfoli", "perfomance", "retrns", "val", "summry",
                "peny stocks", "sctr", "cntry", "rsk", "volatilty", "holdngs", "assest",
                "investmnt", "stoks", "fnds", "prce", "currnt prce", "portflio", "profolio"
            ],
            "news_analysis": [
                # News related - Standard
                "news", "market", "traffic", "impact", "events", "geopolitical", "headlines", 
                "latest", "breaking", "announcement", "update", "current events", "market events",
                # Gen Z Language
                "whats the tea", "spill the tea", "drama", "whats happening", "the scoop", "gossip",
                "whats trending", "viral news", "hot takes", "breaking tea", "market drama",
                "stock drama", "market chaos", "stonk news", "market vibes", "news hits different",
                # Casual/Slang variations
                "whats up with", "whats going on", "whats the deal", "whats new", "any updates",
                "fill me in", "catch me up", "whats the story", "whats the buzz", "whats poppin",
                "market talk", "street talk", "word on the street", "insider info", "market whispers",
                # Question variations
                "how news", "news impact", "market news", "latest news", "current news", "news analysis",
                "news affect", "news influence", "how does news", "news effect", "news impact on",
                "traffic issues", "traffic problems", "traffic affect", "traffic impact", "market impact",
                "how does traffic", "traffic between", "traffic affect stocks", "what happened",
                # Fuzzy/Typo variations
                "nws", "mrket", "trffic", "impct", "evnts", "geopolitcal", "hedlines", "ltest",
                "brking", "announcemnt", "updte", "newz", "markt", "trafic", "impack"
            ],
            "investment_advice": [
                # Investment related - Standard
                "buy", "sell", "hold", "recommendation", "advice", "invest", "opportunity", "strategy",
                "should i", "what to", "where to", "investment advice", "investment tips",
                # Gen Z Language
                "diamond hands", "paper hands", "hodl", "to the moon", "buy the dip", "stonks only go up",
                "yolo", "fomo", "moon mission", "ape in", "send it", "full send", "all in",
                "this is the way", "stonk advice", "investment moves", "money moves", "big brain plays",
                "galaxy brain", "smooth brain", "wrinkled brain", "tendies strategy", "bag advice",
                # Casual/Slang variations
                "what should i do", "help me decide", "give me the play", "whats the move",
                "should i cop", "should i dump", "should i keep", "whats smart", "best move",
                "money advice", "cash advice", "smart plays", "good moves", "winning strategy",
                "make me money", "help me win", "profitable moves", "investment ideas",
                # Question variations
                "what should i buy", "what should i sell", "what should i hold", "should i buy",
                "should i sell", "should i hold", "buy recommendations", "sell recommendations",
                "hold recommendations", "investment suggestions", "investment recommendations",
                "what to buy", "what to sell", "what to hold", "buying advice", "selling advice",
                "holding advice", "investment opportunities", "give me advice", "buying tips", "selling tips",
                # Fuzzy/Typo variations
                "by", "sel", "hol", "recomendatn", "advise", "invest", "opportnity", "stratgy",
                "shuld i", "wat to", "wher to", "recomendation", "advic", "invst"
            ],
            "personal_info": [
                # Personal info related - Standard
                "who", "ganesh", "contact", "work", "experience", "expertise", "background", 
                "company", "role", "about", "tell me about", "who am i", "personal info",
                # Gen Z Language
                "whos this", "who dis", "tell me bout yourself", "your story", "your vibe",
                "who you be", "whats your deal", "bout you", "your background", "spill bout yourself",
                "tell me your tea", "your info", "who are you fr", "no cap who are you",
                "periodt tell me about yourself", "your whole vibe", "main character energy",
                # Casual/Slang variations
                "who are you", "tell me about you", "your info", "your details", "about yourself",
                "introduce yourself", "your profile", "personal details", "contact info",
                "get to know you", "tell me more", "your story", "background info",
                # Question variations
                "who is ganesh", "ganesh divekar", "ganesh contact", "ganesh phone", "ganesh number",
                "ganesh company", "ganesh work", "ganesh role", "about ganesh", "ganesh position",
                "ganesh information", "ganesh details", "tell me about ganesh", "ganesh background",
                "ganesh profile", "ganesh contact number", "ganesh phone number", "ganesh work details",
                "who am i", "my information", "my details", "my profile", "my background",
                "tell me about myself", "my contact", "my work", "my experience", "what is my name",
                "my name", "about me", "tell me about me", "what is my", "my personal", "my info", "my data",
                # Fuzzy/Typo variations
                "ganesh", "ganes", "gansh", "contct", "wrk", "experince", "expertse", "backgrnd",
                "compny", "rol", "abt", "tel me abt", "who am i", "whoami", "whos ganesh"
            ],
            "risk_assessment": [
                # Risk related - Standard
                "risk", "danger", "safe", "volatile", "stability", "security", "protection", "hedge",
                "diversification", "exposure", "risk level", "risk assessment", "portfolio risk", "volatility", "safety",
                # Gen Z Language
                "how risky", "sus investments", "sketchy stocks", "yolo risk", "diamond hands risk",
                "paper hands danger", "moon mission risk", "ape risk", "smooth brain moves",
                "big brain safety", "risk it for the biscuit", "send it safely", "safe plays",
                "risky business", "danger zone", "safe zone", "comfort zone", "scary investments",
                # Casual/Slang variations
                "how safe", "is it safe", "dangerous", "risky stuff", "safe bets", "secure investments",
                "protected money", "hedge my bets", "play it safe", "risky moves", "safe moves",
                "danger level", "safety check", "risk check", "security check", "stable investments",
                # Question variations
                "risk analysis", "risk evaluation", "risk measurement", "risk profile", "risk status",
                "risk overview", "risk summary", "risk report", "volatility analysis", "safety assessment",
                "security analysis", "stability analysis", "exposure analysis", "is my portfolio safe",
                "portfolio safety", "how risky is my portfolio", "portfolio risk level",
                # Fuzzy/Typo variations
                "rsk", "dnger", "sfe", "volatle", "stablty", "securty", "protctn", "hedg",
                "diversifcatn", "exposre", "volatilty", "saftey", "risc", "safty", "stabil"
            ],
            "market_research": [
                # Market research related - Standard
                "research", "analysis", "study", "trends", "market", "industry", "competition",
                "growth", "potential", "outlook", "forecast", "market research", "market analysis",
                # Gen Z Language
                "market tea", "industry vibes", "sector energy", "market mood", "whats trending",
                "market trends", "hot sectors", "fire industries", "lit markets", "booming sectors",
                "market insights", "deep dive", "research vibes", "study the game", "market intel",
                "competition check", "rival analysis", "market drama", "sector gossip",
                # Casual/Slang variations
                "whats hot", "whats popping", "trending markets", "growing sectors", "market buzz",
                "industry talk", "sector news", "market whispers", "growth potential", "market future",
                "competition analysis", "rival check", "market study", "sector study", "trend analysis",
                # Question variations
                "market trends", "market study", "market outlook", "market forecast", "market prediction",
                "market growth", "sector analysis", "industry analysis", "industry trends", "industry research",
                "market insights", "market intelligence", "market data", "market information",
                "sector research", "sector trends", "sector outlook", "sector forecast", "industry study",
                # Fuzzy/Typo variations
                "reserch", "anlysis", "stdy", "trnds", "mrket", "indstry", "competitn", "grwth",
                "potentil", "outlok", "forcast", "resarch", "analisys", "studie", "trends"
            ],
            "technical_analysis": [
                # Technical analysis related - Standard
                "technical", "chart", "pattern", "indicator", "moving average", "rsi", "macd",
                "support", "resistance", "breakout", "trend", "technical analysis", "chart analysis",
                # Gen Z Language
                "chart vibes", "pattern energy", "technical tea", "chart reading", "lines and patterns",
                "support and resistance", "breakout energy", "trend vibes", "chart magic",
                "technical wizardry", "chart game", "pattern game", "indicator vibes", "signal energy",
                "momentum vibes", "trend energy", "chart patterns hit different", "technical stuff",
                # Casual/Slang variations
                "chart stuff", "technical stuff", "pattern stuff", "indicator stuff", "chart reading",
                "pattern reading", "signal reading", "trend reading", "chart interpretation",
                "pattern interpretation", "technical interpretation", "chart signals", "pattern signals",
                # Question variations
                "pattern analysis", "technical indicators", "chart patterns", "technical signals",
                "technical trends", "technical momentum", "rsi analysis", "macd analysis", "support levels",
                "resistance levels", "trend analysis", "momentum analysis", "signal analysis", "technical study",
                "chart study", "pattern study", "indicator analysis", "technical evaluation", "technical charts",
                # Fuzzy/Typo variations
                "techncal", "chrt", "patern", "indictor", "movng avrage", "rs", "mac", "suport",
                "resistance", "breakot", "trnd", "techical", "chart", "patern", "indicater"
            ],
            "sentiment_analysis": [
                # Sentiment related - Standard
                "sentiment", "mood", "feeling", "opinion", "perception", "confidence", "fear", "greed",
                "bullish", "bearish", "market sentiment", "investor sentiment", "market mood",
                # Gen Z Language
                "market vibes", "investor vibes", "sentiment vibes", "mood check", "vibe check",
                "market energy", "investor energy", "bullish energy", "bearish energy", "market feels",
                "investor feels", "sentiment feels", "market emotions", "investor emotions",
                "good vibes", "bad vibes", "positive vibes", "negative vibes", "market psychology",
                "crowd psychology", "herd mentality", "fomo vibes", "fear vibes", "greed vibes",
                # Casual/Slang variations
                "how people feel", "market feelings", "investor feelings", "public opinion", "crowd opinion",
                "market opinion", "investor opinion", "sentiment check", "mood analysis", "feeling analysis",
                "emotion analysis", "psychology analysis", "confidence check", "fear check", "greed check",
                # Question variations
                "sentiment analysis", "social sentiment", "media sentiment", "public sentiment",
                "market feeling", "market emotion", "market psychology", "social media sentiment",
                "market perception", "investor confidence", "market fear", "sentiment study",
                "mood analysis", "market mood analysis", "investor mood analysis", "market psychology analysis",
                # Fuzzy/Typo variations
                "sentimnt", "md", "feeling", "opnion", "perceptn", "confdence", "fr", "gred",
                "bullsh", "bearsh", "mrket sentimnt", "sentment", "moud", "fealing", "opinon"
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
        """Enhanced intent classification with sophisticated pattern matching and context awareness"""
        query_lower = query.lower().strip()
        
        # Enhanced special cases with better pattern matching
        special_cases = self._check_special_cases(query_lower)
        if special_cases:
            return special_cases
        
        # Clean and normalize query
        query_clean = re.sub(r'[^\w\s]', ' ', query_lower)
        query_words = query_clean.split()
        
        # Enhanced scoring with context awareness
        intent_scores = self._calculate_enhanced_scores(query_lower, query_words)
        
        # Find primary intent with confidence threshold
        primary_intent = max(intent_scores.items(), key=lambda x: x[1])
        
        # Get secondary intents (if any have significant scores)
        secondary_intents = [
            intent for intent, score in intent_scores.items() 
            if score > 0.2 and intent != primary_intent[0]  # Increased threshold
        ]
        
        # Enhanced confidence calculation
        confidence = self._calculate_confidence(primary_intent[1], intent_scores, query_lower)
        
        return {
            "primary": primary_intent[0],
            "confidence": confidence,
            "secondary": secondary_intents,
            "all_scores": intent_scores,
            "query_context": self._extract_query_context(query_lower)
        }
    
    def _check_special_cases(self, query_lower: str) -> Optional[Dict[str, Any]]:
        """Check for special cases with enhanced pattern matching"""
        
        # Personal info special cases
        personal_patterns = [
            r'^who\s+am\s+i\s*[?.]*$',
            r'^whoami\s*[?.]*$',
            r'^who\s+am\s+i\s*$',
            r'^tell\s+me\s+about\s+myself\s*[?.]*$',
            r'^my\s+information\s*[?.]*$',
            r'^my\s+details\s*[?.]*$'
        ]
        
        for pattern in personal_patterns:
            if re.match(pattern, query_lower):
                print(f"DEBUG: Personal info special case triggered for query: '{query_lower}'")
                return {
                    "primary": "personal_info",
                    "confidence": 1.0,
                    "secondary": [],
                    "all_scores": {"personal_info": 1.0}
                }
        
        # Portfolio analysis special cases
        portfolio_patterns = [
            r'.*portfolio.*(help|analyze|check|review|show|display|get).*',
            r'.*(help|analyze|check|review|show|display|get).*portfolio.*',
            r'.*my\s+(portfolio|investments|stocks|holdings).*',
            r'.*(portfolio|investments|stocks|holdings)\s+analysis.*',
            r'.*analyze\s+my\s+(portfolio|investments|stocks).*'
        ]
        
        for pattern in portfolio_patterns:
            if re.match(pattern, query_lower):
                print(f"DEBUG: Portfolio analysis special case triggered for query: '{query_lower}'")
                return {
                    "primary": "portfolio_analysis",
                    "confidence": 1.0,
                    "secondary": [],
                    "all_scores": {"portfolio_analysis": 1.0}
                }
        
        # Price queries special cases
        price_patterns = [
            r'.*price.*(current|what|how\s+much|cost).*',
            r'.*(current|what|how\s+much|cost).*price.*',
            r'.*stock\s+price.*',
            r'.*share\s+price.*',
            r'.*current\s+value.*'
        ]
        
        for pattern in price_patterns:
            if re.match(pattern, query_lower):
                print(f"DEBUG: Price query special case triggered for query: '{query_lower}'")
                return {
                    "primary": "portfolio_analysis",
                    "confidence": 1.0,
                    "secondary": [],
                    "all_scores": {"portfolio_analysis": 1.0}
                }
        
        # Enlist queries special cases
        enlist_patterns = [
            r'.*enlist\s+(stocks|sectors|countries).*',
            r'.*list\s+(stocks|sectors|countries).*',
            r'.*show\s+(stocks|sectors|countries).*',
            r'.*(all|my)\s+(stocks|sectors|countries).*',
            r'.*(stocks|sectors|countries)\s+list.*'
        ]
        
        for pattern in enlist_patterns:
            if re.match(pattern, query_lower):
                print(f"DEBUG: Enlist query special case triggered for query: '{query_lower}'")
                return {
                    "primary": "portfolio_analysis",
                    "confidence": 1.0,
                    "secondary": [],
                    "all_scores": {"portfolio_analysis": 1.0}
                }
        
        return None
    
    def _calculate_enhanced_scores(self, query_lower: str, query_words: List[str]) -> Dict[str, float]:
        """Calculate enhanced intent scores with context awareness and weighted patterns"""
        intent_scores = {}
        
        for intent_name, patterns in self.intent_patterns.items():
            score = 0
            total_patterns = len(patterns)
            
            for pattern in patterns:
                # Exact match (highest score)
                if pattern == query_lower.strip():
                    score += 3.0
                elif pattern in query_lower:
                    score += 2.0
                # Partial word match (medium score)
                elif any(word in pattern for word in query_words):
                    score += 1.5
                # Word similarity (lower score for typos)
                elif self._word_similarity(pattern, query_words):
                    score += 1.0
            
            # Context bonus for specific patterns
            context_bonus = self._calculate_context_bonus(intent_name, query_lower)
            score += context_bonus
            
            # Normalize score
            intent_scores[intent_name] = score / total_patterns if total_patterns > 0 else 0
        
        return intent_scores
    
    def _calculate_context_bonus(self, intent_name: str, query_lower: str) -> float:
        """Calculate context bonus based on query patterns"""
        bonus = 0.0
        
        # Question words bonus
        question_words = ['what', 'how', 'why', 'when', 'where', 'which', 'who']
        if any(word in query_lower for word in question_words):
            bonus += 0.5
        
        # Action words bonus
        action_words = ['help', 'analyze', 'check', 'review', 'show', 'tell', 'explain']
        if any(word in query_lower for word in action_words):
            bonus += 0.3
        
        # Intent-specific bonuses
        if intent_name == "portfolio_analysis" and "my" in query_lower:
            bonus += 0.4
        elif intent_name == "personal_info" and ("who" in query_lower or "about" in query_lower):
            bonus += 0.4
        elif intent_name == "investment_advice" and ("should" in query_lower or "recommend" in query_lower):
            bonus += 0.4
        
        return bonus
    
    def _calculate_confidence(self, primary_score: float, all_scores: Dict[str, float], query_lower: str) -> float:
        """Calculate confidence based on score difference and query complexity"""
        # Base confidence from primary score
        confidence = min(primary_score, 1.0)
        
        # Boost confidence if primary score is significantly higher than others
        other_scores = [score for intent, score in all_scores.items() if score != primary_score]
        if other_scores:
            max_other = max(other_scores)
            if primary_score > max_other * 1.5:  # 50% higher than next best
                confidence = min(confidence * 1.2, 1.0)
        
        # Reduce confidence for ambiguous queries
        if len([score for score in all_scores.values() if score > 0.3]) > 2:
            confidence *= 0.8
        
        return confidence
    
    def _extract_query_context(self, query_lower: str) -> Dict[str, Any]:
        """Extract context information from the query"""
        context = {
            "is_question": any(word in query_lower for word in ['what', 'how', 'why', 'when', 'where', 'which', 'who', '?']),
            "has_action_words": any(word in query_lower for word in ['help', 'analyze', 'check', 'review', 'show', 'tell', 'explain']),
            "has_ownership": 'my' in query_lower or 'mine' in query_lower,
            "query_length": len(query_lower.split()),
            "complexity": "complex" if len(query_lower.split()) > 5 else "simple"
        }
        return context
    
    def _word_similarity(self, pattern: str, query_words: list) -> bool:
        """Enhanced word similarity check to handle typos, variations, and fuzzy matching"""
        pattern_words = pattern.split()
        
        for word in query_words:
            for pattern_word in pattern_words:
                if len(word) >= 2 and len(pattern_word) >= 2:
                    # Exact substring match
                    if word in pattern_word or pattern_word in word:
                        return True
                    
                    # Length-based fuzzy matching
                    if len(word) >= 3 and len(pattern_word) >= 3:
                        # Allow character differences based on word length
                        max_diff = max(1, min(len(word), len(pattern_word)) // 3)
                        
                        if abs(len(word) - len(pattern_word)) <= max_diff:
                            diff_count = sum(1 for a, b in zip(word, pattern_word) if a != b)
                            if diff_count <= max_diff:
                                return True
                    
                    # Check for common character swaps (transpositions)
                    if self._check_transposition(word, pattern_word):
                        return True
                    
                    # Check for common misspellings and variations
                    if self._is_common_misspelling(word, pattern_word):
                        return True
                    
                    # Check for phonetic similarity (basic)
                    if self._phonetic_similarity(word, pattern_word):
                        return True
        
        return False
    
    def _check_transposition(self, word1: str, word2: str) -> bool:
        """Check for character transposition (swapped adjacent characters)"""
        if abs(len(word1) - len(word2)) > 1:
            return False
            
        if len(word1) == len(word2):
            diff_positions = [i for i in range(len(word1)) if word1[i] != word2[i]]
            if len(diff_positions) == 2:
                i, j = diff_positions
                if abs(i - j) == 1:  # Adjacent positions
                    return word1[i] == word2[j] and word1[j] == word2[i]
        
        return False
    
    def _phonetic_similarity(self, word1: str, word2: str) -> bool:
        """Basic phonetic similarity check"""
        # Common phonetic replacements
        phonetic_map = {
            'c': 'k', 'k': 'c', 'f': 'ph', 'ph': 'f',
            'z': 's', 's': 'z', 'i': 'y', 'y': 'i'
        }
        
        for char, replacement in phonetic_map.items():
            if char in word1.lower() and replacement in word2.lower():
                if word1.lower().replace(char, replacement) == word2.lower():
                    return True
            if char in word2.lower() and replacement in word1.lower():
                if word2.lower().replace(char, replacement) == word1.lower():
                    return True
        
        return False
    
    def _is_common_misspelling(self, word: str, pattern: str) -> bool:
        """Enhanced common misspellings and variations check"""
        # Comprehensive misspellings dictionary
        common_misspellings = {
            # Portfolio related
            "portfolio": ["portfolo", "portfollio", "portfoli", "portflio", "profolio", "porfolio"],
            "performance": ["perfomance", "perfrmance", "preformance", "performence"],
            "summary": ["summry", "sumary", "sumery", "summery"],
            "stocks": ["stoks", "stonks", "stokcs", "stockz"],
            "investment": ["investmnt", "invesment", "investement", "investmnet"],
            
            # News related
            "news": ["nws", "newz", "new", "newss"],
            "market": ["mrket", "markt", "markeet", "markett"],
            "traffic": ["trffic", "trafik", "trafic", "traffik"],
            "impact": ["impct", "impackt", "impakt", "imapct"],
            
            # Analysis related
            "analysis": ["anlysis", "analisis", "analisys", "anaylsis"],
            "research": ["reserch", "recherch", "resarch", "reseach"],
            "technical": ["techncal", "techical", "tecnical", "technicall"],
            "sentiment": ["sentimnt", "sentment", "sentimant", "sentyment"],
            
            # Investment advice
            "recommendation": ["recomendatn", "recomendation", "recomandation", "recomendashun"],
            "advice": ["advise", "advic", "advis", "advices"],
            "buy": ["by", "byu", "buuy", "byy"],
            "sell": ["sel", "seel", "sall", "cell"],
            "hold": ["hol", "hoold", "hhold", "holdd"],
            
            # Personal info
            "ganesh": ["ganes", "gansh", "ganeshh", "ganessh"],
            "contact": ["contct", "contakt", "contak", "contac"],
            "who": ["woh", "whoo", "hwo", "wo"],
            
            # Risk related
            "risk": ["rsk", "risc", "riskk", "risck"],
            "volatility": ["volatilty", "volatality", "volatlity", "volatilityy"],
            "safety": ["saftey", "safte", "safty", "saftty"],
            "danger": ["dnger", "dangr", "dangerr", "dager"],
            
            # Market research
            "trends": ["trnds", "trend", "trendz", "trendd"],
            "industry": ["indstry", "industy", "industrie", "industryy"],
            "competition": ["competitn", "competishun", "competetion", "compettion"],
            "growth": ["grwth", "growht", "growtth", "growthh"],
            
            # Gen Z variations
            "stonks": ["stocks", "stoks", "stonk", "stonkz"],
            "hodl": ["hold", "hol", "hodll", "hodl"],
            "tendies": ["tenders", "tendys", "tendiez", "tendees"],
            "vibes": ["vibe", "vibez", "vybes", "vibs"],
            "tea": ["t", "tee", "teaa", "teea"]
        }
        
        # Check both directions (word->pattern and pattern->word)
        word_lower = word.lower()
        pattern_lower = pattern.lower()
        
        # Direct lookup
        if pattern_lower in common_misspellings:
            if word_lower in common_misspellings[pattern_lower]:
                return True
        
        if word_lower in common_misspellings:
            if pattern_lower in common_misspellings[word_lower]:
                return True
        
        # Reverse lookup (check if word is a correct spelling of a misspelled pattern)
        for correct_word, misspellings in common_misspellings.items():
            if pattern_lower in misspellings and word_lower == correct_word:
                return True
            if word_lower in misspellings and pattern_lower == correct_word:
                return True
        
        return False
    
    def _route_to_agents(self, query: str, intent: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Enhanced routing with intelligent agent selection and context awareness"""
        agent_responses = {}
        
        # Enhanced primary agent routing with confidence check
        primary_agent = self._get_agent_for_intent(intent["primary"])
        if primary_agent and intent["confidence"] > 0.25:  # Lowered minimum confidence threshold
            try:
                # Enhanced query processing with context
                enhanced_query = self._enhance_query_with_context(query, intent)
                response = primary_agent.process({
                    "query": enhanced_query,
                    "language": language,
                    "context": intent.get("query_context", {})
                })
                agent_responses[intent["primary"]] = response
            except Exception as e:
                print(f"Error in {intent['primary']} agent: {e}")
                agent_responses[intent["primary"]] = {
                    "agent": intent["primary"].replace("_", " ").title(),
                    "response": "Sorry, I couldn't process this request. Please try rephrasing your question.",
                    "type": "error"
                }
        
        # Smart secondary agent routing
        for secondary_intent in intent["secondary"]:
            if intent["all_scores"][secondary_intent] > 0.4:  # Higher threshold for secondary agents
                secondary_agent = self._get_agent_for_intent(secondary_intent)
                if secondary_agent and self._should_route_to_secondary(query, intent, secondary_intent):
                    try:
                        enhanced_query = self._enhance_query_with_context(query, intent)
                        response = secondary_agent.process({
                            "query": enhanced_query,
                            "language": language,
                            "context": intent.get("query_context", {})
                        })
                        agent_responses[secondary_intent] = response
                    except Exception as e:
                        print(f"Error in {secondary_intent} agent: {e}")
        
        # Enhanced fallback with better error handling
        if not agent_responses:
            fallback_agent = self.agents["rag_agent"]
            try:
                response = fallback_agent.process({
                    "query": query,
                    "language": language,
                    "context": {"fallback": True, "original_intent": intent["primary"]}
                })
                agent_responses["fallback"] = response
            except Exception as e:
                print(f"Error in fallback agent: {e}")
                agent_responses["fallback"] = {
                    "agent": "RAG Agent",
                    "response": "I'm sorry, I couldn't understand your request. Could you please rephrase it or ask about your portfolio, investments, or personal information?",
                    "type": "error"
                }
        
        return agent_responses
    
    def _enhance_query_with_context(self, query: str, intent: Dict[str, Any]) -> str:
        """Enhance query with context information for better agent processing"""
        context = intent.get("query_context", {})
        
        # Add context hints to the query
        enhanced_query = query
        
        if context.get("is_question"):
            enhanced_query += " [QUESTION]"
        
        if context.get("has_action_words"):
            enhanced_query += " [ACTION_REQUEST]"
        
        if context.get("has_ownership"):
            enhanced_query += " [PERSONAL_REQUEST]"
        
        return enhanced_query
    
    def _should_route_to_secondary(self, query: str, intent: Dict[str, Any], secondary_intent: str) -> bool:
        """Determine if query should be routed to secondary agent"""
        # Don't route if primary confidence is very high
        if intent["confidence"] > 0.8:
            return False
        
        # Route if secondary intent is complementary
        complementary_pairs = [
            ("portfolio_analysis", "risk_assessment"),
            ("portfolio_analysis", "investment_advice"),
            ("investment_advice", "market_research"),
            ("investment_advice", "technical_analysis"),
            ("news_analysis", "sentiment_analysis")
        ]
        
        primary = intent["primary"]
        if (primary, secondary_intent) in complementary_pairs or (secondary_intent, primary) in complementary_pairs:
            return True
        
        # Route if query is complex (longer than 5 words)
        if len(query.split()) > 5:
            return True
        
        return False
    
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

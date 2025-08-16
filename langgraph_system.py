from typing import Dict, Any, List, TypedDict
from agents import MasterAgent
import json

# Define state structure
class AgentState(TypedDict):
    query: str
    user_language: str
    agent_responses: List[Dict[str, Any]]
    current_agent: str
    final_response: str
    should_continue: bool

class FinancialAgentSystem:
    """Main system orchestrating multiple financial analysis agents"""
    
    def __init__(self):
        self.master_agent = MasterAgent()
    
    # Simplified system with Master Agent orchestration
    
    def _classify_query(self, query: str) -> List[str]:
        """Classify the query and determine which agents to run"""
        query_lower = query.lower()
        
        # Determine which agents should process this query
        agents_to_run = []
        
        # Portfolio-related queries
        if any(keyword in query_lower for keyword in [
            "portfolio", "performance", "returns", "value", "summary",
            "penny stocks", "sector", "country", "risk", "volatility"
        ]):
            agents_to_run.append("portfolio_analysis")
        
        # News-related queries
        if any(keyword in query_lower for keyword in [
            "news", "market", "traffic", "impact", "events", "geopolitical"
        ]):
            agents_to_run.append("news_analysis")
        
        # Investment advice queries
        if any(keyword in query_lower for keyword in [
            "buy", "sell", "hold", "recommendation", "advice", "invest",
            "opportunity", "strategy"
        ]):
            agents_to_run.append("investment_advice")
        
        # General questions about the user
        if any(keyword in query_lower for keyword in [
            "who", "ganesh", "contact", "work", "experience", "expertise",
            "background", "company", "role"
        ]):
            agents_to_run.append("rag_response")
        
        # If no specific classification, run all agents
        if not agents_to_run:
            agents_to_run = ["portfolio_analysis", "news_analysis", "investment_advice", "rag_response"]
        
        return agents_to_run
    

    
    def _combine_responses(self, responses: List[Dict[str, Any]], language: str) -> str:
        """Combine multiple agent responses into a coherent response"""
        if language == "genz":
            combined = "🤖 Multi-Agent Analysis Complete! 🤖\n\n"
            
            for i, response in enumerate(responses, 1):
                agent_name = response.get("agent", f"Agent {i}")
                agent_response = response.get("response", "")
                
                combined += f"📊 {agent_name}:\n{agent_response}\n"
                
                if i < len(responses):
                    combined += "─" * 50 + "\n"
        else:
            combined = "Multi-Agent Analysis Complete!\n\n"
            
            for i, response in enumerate(responses, 1):
                agent_name = response.get("agent", f"Agent {i}")
                agent_response = response.get("response", "")
                
                combined += f"{agent_name}:\n{agent_response}\n"
                
                if i < len(responses):
                    combined += "-" * 50 + "\n"
        
        return combined
    
    def process_query(self, query: str, language: str = "normal") -> Dict[str, Any]:
        """Process a user query through the master agent system"""
        try:
            # Use master agent for intent classification and routing
            master_response = self.master_agent.process({
                "query": query,
                "language": language
            })
            
            return {
                "success": True,
                "response": master_response["response"],
                "agent_responses": list(master_response["data"]["agent_responses"].values()),
                "query": query,
                "language": language,
                "intent_analysis": master_response["data"]["intent"],
                "routing_info": master_response["data"]["routing_info"]
            }
            
        except Exception as e:
            print(f"Error processing query: {e}")
            return {
                "success": False,
                "response": "I'm sorry, I encountered an error processing your request. Please try again.",
                "error": str(e),
                "query": query,
                "language": language
            }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents"""
        return {
            "portfolio_analyzer": self.portfolio_agent.get_status(),
            "news_analyzer": self.news_agent.get_status(),
            "investment_advisor": self.investment_agent.get_status(),
            "rag_agent": self.rag_agent.get_status()
        }

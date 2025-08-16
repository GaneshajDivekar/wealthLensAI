from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from data.user_profile import get_user_info, get_knowledge_base
from config import Config

class RAGAgent(BaseAgent):
    """Agent for answering general questions about the user using RAG"""
    
    def __init__(self):
        super().__init__(
            name="RAG Agent",
            description="Answers general questions about the user using Retrieval Augmented Generation"
        )
        self.setup_simple_db()
    
    def setup_simple_db(self):
        """Setup simple knowledge base without vector database"""
        try:
            self.knowledge_base = get_knowledge_base()
            self.user_info = get_user_info()
            self.collection = True  # Simple flag
        except Exception as e:
            print(f"Error setting up knowledge base: {e}")
            self.collection = None
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process RAG query"""
        query = input_data.get("query", "")
        user_language = input_data.get("language", "normal")
        
        if not self.collection:
            return self._fallback_response(query, user_language)
        
        try:
            # Simple keyword-based search
            response = self._simple_search(query, user_language)
            
            return {
                "agent": self.name,
                "response": response + "\n\n👤 Source: RAG Agent (Personal Info)",
                "data": {
                    "query": query,
                    "method": "simple_search"
                },
                "type": "rag_response"
            }
            
        except Exception as e:
            print(f"Error in RAG processing: {e}")
            return self._fallback_response(query, user_language)
    
    def _simple_search(self, query: str, language: str) -> str:
        """Simple keyword-based search"""
        query_lower = query.lower()
        
        # Search in knowledge base
        for qa in self.knowledge_base:
            if any(keyword in query_lower for keyword in qa['question'].lower().split()):
                return self._format_response(qa['answer'], language)
        
        # If no match found, use fallback
        return self._fallback_response(query, language)
    
    def _format_response(self, answer: str, language: str) -> str:
        """Format response based on language preference"""
        if language == "genz":
            return f"💡 {answer}"
        else:
            return answer
    
    def _fallback_response(self, query: str, language: str) -> str:
        """Fallback response when RAG fails"""
        user_info = get_user_info()
        query_lower = query.lower()
        
        # Simple keyword-based responses
        if "who" in query_lower and "ganesh" in query_lower:
            if language == "genz":
                return f"""
                👨‍💼 About Ganesh Divekar 👨‍💼
                
                🏢 Works at: {user_info['personal_info']['company']}
                💼 Role: {user_info['personal_info']['role']}
                📞 Contact: {user_info['personal_info']['contact']}
                ⏰ Experience: {user_info['personal_info']['experience_years']} years
                🎯 Specialization: {user_info['personal_info']['specialization']}
                """
            else:
                return f"""
                About Ganesh Divekar:
                
                Works at: {user_info['personal_info']['company']}
                Role: {user_info['personal_info']['role']}
                Contact: {user_info['personal_info']['contact']}
                Experience: {user_info['personal_info']['experience_years']} years
                Specialization: {user_info['personal_info']['specialization']}
                """
        
        elif "contact" in query_lower or "phone" in query_lower or "number" in query_lower:
            if language == "genz":
                return f"📞 Contact Ganesh at: {user_info['personal_info']['contact']}"
            else:
                return f"You can contact Ganesh at: {user_info['personal_info']['contact']}"
        
        elif "work" in query_lower or "company" in query_lower:
            if language == "genz":
                return f"🏢 Ganesh works at {user_info['personal_info']['company']} as {user_info['personal_info']['role']}"
            else:
                return f"Ganesh works at {user_info['personal_info']['company']} as {user_info['personal_info']['role']}"
        
        elif "experience" in query_lower or "years" in query_lower:
            if language == "genz":
                return f"⏰ Ganesh has {user_info['personal_info']['experience_years']} years of experience in {user_info['personal_info']['specialization']}"
            else:
                return f"Ganesh has {user_info['personal_info']['experience_years']} years of experience in {user_info['personal_info']['specialization']}"
        
        elif "portfolio" in query_lower or "investment" in query_lower:
            if language == "genz":
                return f"""
                💰 Investment Philosophy 💰
                
                {', '.join(user_info['investment_philosophy'])}
                
                📊 Portfolio Preferences:
                {', '.join(user_info['portfolio_preferences'])}
                """
            else:
                return f"""
                Investment Philosophy:
                {', '.join(user_info['investment_philosophy'])}
                
                Portfolio Preferences:
                {', '.join(user_info['portfolio_preferences'])}
                """
        
        elif "expertise" in query_lower or "skills" in query_lower:
            if language == "genz":
                return f"""
                🎯 Expertise Areas 🎯
                
                {', '.join(user_info['expertise_areas'])}
                """
            else:
                return f"""
                Expertise Areas:
                {', '.join(user_info['expertise_areas'])}
                """
        
        else:
            if language == "genz":
                return f"""
                🤖 I'm here to help with questions about Ganesh Divekar!
                
                💡 You can ask about:
                • Who is Ganesh?
                • Contact information
                • Work and experience
                • Portfolio and investments
                • Expertise and skills
                • Professional background
                """
            else:
                return f"""
                I'm here to help with questions about Ganesh Divekar!
                
                You can ask about:
                • Who is Ganesh?
                • Contact information
                • Work and experience
                • Portfolio and investments
                • Expertise and skills
                • Professional background
                """

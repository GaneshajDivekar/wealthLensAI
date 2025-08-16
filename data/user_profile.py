from typing import List, Dict

# User Profile Data for WealthLens RAG System
USER_PROFILE = {
    "personal_info": {
        "name": "Ganesh Divekar",
        "company": "Bajaj Technology",
        "role": "Leading India USA Mideast AI Team",
        "contact": "8459684546",
        "location": "India",
        "experience_years": 8,
        "specialization": "AI/ML, Financial Technology, Team Leadership"
    },
    "professional_background": [
        "Leading AI teams across India, USA, and Middle East regions",
        "Expertise in machine learning, deep learning, and AI applications",
        "Experience in financial technology and portfolio management",
        "Strong background in team leadership and project management",
        "Knowledge of both Indian and US financial markets"
    ],
    "investment_philosophy": [
        "Long-term value investing approach",
        "Diversification across sectors and geographies",
        "Focus on both large-cap stability and small-cap growth opportunities",
        "Technology sector expertise with emphasis on AI and digital transformation",
        "Balanced portfolio with Indian and US exposure"
    ],
    "portfolio_preferences": [
        "Prefers technology and banking sectors",
        "Invests in both Indian and US markets",
        "Includes penny stocks for high growth potential",
        "Maintains mutual fund investments for diversification",
        "Portfolio value around 80 lacs INR"
    ],
    "expertise_areas": [
        "Artificial Intelligence and Machine Learning",
        "Financial Technology and Algorithmic Trading",
        "Team Leadership and Cross-cultural Management",
        "Portfolio Analysis and Risk Management",
        "Market Research and Investment Strategy"
    ],
    "interests": [
        "AI and emerging technologies",
        "Financial markets and investment strategies",
        "Team building and leadership development",
        "Cross-border business opportunities",
        "Innovation in fintech solutions"
    ]
}

# Knowledge base for RAG
KNOWLEDGE_BASE = [
    {
        "question": "Who is Ganesh Divekar?",
        "answer": "Ganesh Divekar is a technology leader working at Bajaj Technology, leading AI teams across India, USA, and Middle East regions. He has 8+ years of experience in AI/ML and financial technology."
    },
    {
        "question": "What is Ganesh's role?",
        "answer": "Ganesh is leading the India USA Mideast AI Team at Bajaj Technology, focusing on AI/ML applications and team leadership across multiple regions."
    },
    {
        "question": "How can I contact Ganesh?",
        "answer": "You can contact Ganesh Divekar at 8459684546. He is based in India and works with Bajaj Technology."
    },
    {
        "question": "What is Ganesh's investment strategy?",
        "answer": "Ganesh follows a long-term value investing approach with diversification across sectors and geographies. His portfolio includes both Indian and US stocks, with focus on technology and banking sectors."
    },
    {
        "question": "What is Ganesh's portfolio value?",
        "answer": "Ganesh's portfolio is valued at approximately 80 lacs INR, including stocks from both Indian and US markets, along with mutual fund investments."
    },
    {
        "question": "What sectors does Ganesh invest in?",
        "answer": "Ganesh primarily invests in technology and banking sectors, with exposure to both large-cap stability stocks and small-cap growth opportunities including penny stocks."
    },
    {
        "question": "What is Ganesh's expertise?",
        "answer": "Ganesh specializes in AI/ML, financial technology, team leadership, portfolio analysis, and risk management. He has strong expertise in cross-cultural team management."
    },
    {
        "question": "Where does Ganesh work?",
        "answer": "Ganesh works at Bajaj Technology, leading AI teams across India, USA, and Middle East regions."
    },
    {
        "question": "What is Ganesh's experience level?",
        "answer": "Ganesh has over 8 years of experience in AI/ML and financial technology, with expertise in leading cross-border teams."
    },
    {
        "question": "What are Ganesh's interests?",
        "answer": "Ganesh is interested in AI and emerging technologies, financial markets, investment strategies, team building, and innovation in fintech solutions."
    }
]

def get_user_info():
    """Get user information"""
    return USER_PROFILE

def get_knowledge_base():
    """Get knowledge base for RAG"""
    return KNOWLEDGE_BASE

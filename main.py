from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn
from langgraph_system import FinancialAgentSystem
from services.chart_service import chart_service
from services.real_time_data import real_time_service
from data.portfolio_data import get_portfolio_data
from data import get_portfolio_summary, PORTFOLIO_DATA
import uuid
from datetime import datetime
import json

# Initialize FastAPI app
app = FastAPI(
    title="WealthLens - AI Financial Portfolio Analysis System",
    description="AI-powered financial portfolio analysis with multiple agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent system
agent_system = FinancialAgentSystem()

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = "normal"  # "normal" or "genz"
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str
    success: bool
    agent_responses: Optional[List[Dict[str, Any]]] = None
    sources: Optional[List[str]] = None
    intent: Optional[str] = None

class PortfolioRequest(BaseModel):
    analysis_type: Optional[str] = "summary"  # "summary", "detailed", "sectors", "countries"

class PortfolioResponse(BaseModel):
    data: Dict[str, Any]
    summary: Dict[str, Any]
    timestamp: str

class AgentStatusResponse(BaseModel):
    agents: Dict[str, Any]
    system_status: str
    timestamp: str

# In-memory session storage (in production, use Redis or database)
sessions = {}

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "WealthLens - AI Financial Portfolio Analysis System API",
        "version": "1.0.0",
        "status": "running",
        "authentication": "disabled",
        "endpoints": {
            "chat": "/chat",
            "portfolio": "/portfolio",
            "agents": "/agents/status",
            "health": "/health",
            "examples": "/examples"
        },
        "demo_mode": True
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint for portfolio analysis"""
    try:
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Process query through agent system
        result = agent_system.process_query(request.message, request.language)
        
        # Store session data
        sessions[session_id] = {
            "user": "demo",
            "last_query": request.message,
            "last_response": result["response"],
            "timestamp": datetime.now().isoformat(),
            "language": request.language
        }
        
        return ChatResponse(
            response=result["response"],
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            success=result["success"],
            agent_responses=result.get("agent_responses", []),
            sources=result.get("routing_info", {}).get("agents_used", []),
            intent=result.get("intent_analysis", {}).get("primary", "unknown")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.get("/portfolio", response_model=PortfolioResponse)
async def get_portfolio(analysis_type: str = "summary"):
    """Get portfolio analysis"""
    try:
        summary = get_portfolio_summary()
        
        if analysis_type == "summary":
            data = {
                "summary": summary,
                "total_stocks": len(PORTFOLIO_DATA["stocks"]),
                "total_mutual_funds": len(PORTFOLIO_DATA["mutual_funds"])
            }
        elif analysis_type == "detailed":
            data = {
                "summary": summary,
                "stocks": PORTFOLIO_DATA["stocks"],
                "mutual_funds": PORTFOLIO_DATA["mutual_funds"]
            }
        elif analysis_type == "sectors":
            sectors = {}
            for stock in PORTFOLIO_DATA["stocks"]:
                sector = stock["sector"]
                if sector not in sectors:
                    sectors[sector] = {"stocks": [], "total_value": 0}
                sectors[sector]["stocks"].append(stock)
                sectors[sector]["total_value"] += stock["quantity"] * stock["current_price"]
            
            data = {
                "summary": summary,
                "sectors": sectors
            }
        elif analysis_type == "countries":
            countries = {}
            for stock in PORTFOLIO_DATA["stocks"]:
                country = stock["country"]
                if country not in countries:
                    countries[country] = {"stocks": [], "total_value": 0}
                countries[country]["stocks"].append(stock)
                countries[country]["total_value"] += stock["quantity"] * stock["current_price"]
            
            data = {
                "summary": summary,
                "countries": countries
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid analysis type")
        
        return PortfolioResponse(
            data=data,
            summary=summary,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting portfolio: {str(e)}")

@app.get("/portfolio/penny-stocks")
async def get_penny_stocks():
    """Get penny stocks in portfolio"""
    try:
        penny_stocks = [stock for stock in PORTFOLIO_DATA["stocks"] if stock["current_price"] < 20]
        
        return {
            "penny_stocks": penny_stocks,
            "count": len(penny_stocks),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting penny stocks: {str(e)}")

@app.get("/agents/status", response_model=AgentStatusResponse)
async def get_agent_status():
    """Get status of all agents"""
    try:
        return AgentStatusResponse(
            agents=agent_system.master_agent.get_agent_status(),
            system_status="running",
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting agent status: {str(e)}")

@app.get("/agents/list")
async def list_agents():
    """List all available agents"""
    try:
        agents = agent_system.master_agent.get_agent_status()
        return {
            "agents": list(agents.keys()),
            "total_agents": len(agents),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing agents: {str(e)}")

@app.post("/intent-analysis")
async def analyze_intent(request: ChatRequest):
    """Analyze intent of a query"""
    try:
        intent_analysis = agent_system.master_agent._classify_intent(request.message)
        return {
            "query": request.message,
            "intent_analysis": intent_analysis,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing intent: {str(e)}")

@app.get("/sources")
async def get_sources():
    """Get source information for queries"""
    try:
        return {
            "available_sources": [
                "Portfolio Analyzer",
                "Investment Advisor", 
                "Risk Analyzer",
                "Market Research",
                "Technical Analyzer",
                "Sentiment Analyzer",
                "News Analyzer",
                "RAG Agent"
            ],
            "total_sources": 8,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sources: {str(e)}")

@app.get("/examples")
async def get_examples():
    """Get example queries for testing"""
    return {
        "portfolio_analysis": [
            "Show me my portfolio summary",
            "What is my portfolio value?",
            "Analyze my portfolio performance",
            "Show sector breakdown",
            "What are my penny stocks?"
        ],
        "investment_advice": [
            "What should I buy?",
            "Give me investment recommendations",
            "What should I sell?",
            "What should I hold?",
            "Analyze my investment strategy"
        ],
        "risk_assessment": [
            "What is my portfolio risk level?",
            "Analyze my portfolio risk",
            "How diversified is my portfolio?",
            "What are the risk factors?"
        ],
        "market_research": [
            "Market research on my sectors",
            "Industry analysis",
            "Market trends",
            "Growth analysis"
        ],
        "technical_analysis": [
            "Technical analysis of my stocks",
            "Chart patterns",
            "Technical indicators",
            "Support and resistance levels"
        ],
        "sentiment_analysis": [
            "Market sentiment analysis",
            "Investor sentiment",
            "Social media sentiment",
            "Market psychology"
        ],
        "news_analysis": [
            "How does traffic issues between India and USA affect my stocks?",
            "News impact on my portfolio",
            "Event-driven analysis",
            "Market reaction to news"
        ],
        "personal_info": [
            "Who am I?",
            "Tell me about Ganesh Divekar",
            "What is Ganesh's contact number?",
            "Who is Ganesh?"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents": len(agent_system.master_agent.get_agent_status()),
        "authentication": "disabled"
    }

# Chart and data endpoints
@app.get("/charts/portfolio")
async def get_portfolio_charts():
    """Get portfolio charts"""
    try:
        portfolio_data = get_portfolio_data()
        charts = chart_service.generate_portfolio_charts(portfolio_data)
        return {
            "charts": charts,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating charts: {str(e)}")

@app.get("/charts/stock/{symbol}")
async def get_stock_charts(symbol: str):
    """Get stock-specific charts"""
    try:
        charts = chart_service.generate_stock_charts(symbol)
        return {
            "symbol": symbol,
            "charts": charts,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating stock charts: {str(e)}")

@app.get("/data/live-prices")
async def get_live_prices():
    """Get live stock prices"""
    try:
        prices = real_time_service.get_live_prices()
        return {
            "prices": prices,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching live prices: {str(e)}")

@app.get("/data/stock-info/{symbol}")
async def get_stock_info(symbol: str):
    """Get comprehensive stock information"""
    try:
        info = real_time_service.get_comprehensive_stock_info(symbol)
        return {
            "symbol": symbol,
            "info": info,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock info: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

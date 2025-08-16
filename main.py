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
    title="Financial Portfolio Analysis System",
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
        "endpoints": {
            "chat": "/chat",
            "portfolio": "/portfolio",
            "agents": "/agents/status",
            "health": "/health"
        }
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

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents": len(agent_system.master_agent.get_agent_status())
    }

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session information"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "data": sessions[session_id]
    }

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete session"""
    if session_id in sessions:
        del sessions[session_id]
        return {"message": "Session deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@app.get("/examples")
async def get_example_queries():
    """Get example queries for users"""
    return {
        "portfolio_queries": [
            "Show me my portfolio summary",
            "What are my penny stocks?",
            "Analyze my portfolio performance",
            "Show sector breakdown",
            "What's my portfolio value?"
        ],
        "investment_queries": [
            "What should I buy?",
            "Give me investment recommendations",
            "Where should I invest?",
            "What stocks should I sell?",
            "Hold recommendations"
        ],
        "news_queries": [
            "How does news affect my portfolio?",
            "Market news analysis",
            "Traffic issues impact on stocks",
            "Sector news"
        ],
        "risk_queries": [
            "Analyze my portfolio risk",
            "What's my risk level?",
            "Risk assessment",
            "Portfolio volatility"
        ],
        "technical_queries": [
            "Technical analysis of my stocks",
            "Chart patterns",
            "RSI analysis",
            "Support and resistance levels"
        ],
        "sentiment_queries": [
            "Market sentiment analysis",
            "Social media sentiment",
            "Investor mood",
            "Sentiment trends"
        ],
        "market_research_queries": [
            "Market research on my sectors",
            "Industry analysis",
            "Market trends",
            "Sector outlook"
        ],
        "personal_queries": [
            "Who is Ganesh Divekar?",
            "What's Ganesh's contact number?",
            "Tell me about Ganesh's work",
            "What's Ganesh's expertise?"
        ],
        "language_options": [
            "normal",
            "genz"
        ]
    }

@app.post("/intent-analysis")
async def analyze_intent(request: ChatRequest):
    """Analyze intent of a query"""
    try:
        intent_analysis = agent_system.master_agent.get_intent_analysis(request.message)
        return {
            "query": request.message,
            "intent_analysis": intent_analysis,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing intent: {str(e)}")

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

@app.post("/sources")
async def get_sources_for_query(request: ChatRequest):
    """Get source information for a query"""
    try:
        intent_analysis = agent_system.master_agent.get_intent_analysis(request.message)
        agent_mapping = {
            "portfolio_analysis": "Portfolio Analyzer",
            "news_analysis": "News Analyzer", 
            "investment_advice": "Investment Advisor",
            "personal_info": "RAG Agent",
            "risk_assessment": "Risk Analyzer",
            "market_research": "Market Research",
            "technical_analysis": "Technical Analyzer",
            "sentiment_analysis": "Sentiment Analyzer"
        }
        
        primary_intent = intent_analysis["intent_analysis"]["primary"]
        primary_agent = agent_mapping.get(primary_intent, "Unknown")
        
        return {
            "query": request.message,
            "primary_intent": primary_intent,
            "primary_agent": primary_agent,
            "confidence": intent_analysis["intent_analysis"]["confidence"],
            "all_intents": intent_analysis["intent_analysis"]["all_scores"],
            "agent_mapping": agent_mapping,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sources: {str(e)}")

@app.get("/charts/portfolio")
async def get_portfolio_charts():
    """Get portfolio charts"""
    try:
        portfolio_data = get_portfolio_data()
        
        pie_chart = chart_service.generate_portfolio_pie_chart(portfolio_data)
        performance_chart = chart_service.generate_portfolio_performance_chart(portfolio_data)
        risk_chart = chart_service.generate_risk_metrics_chart(portfolio_data)
        sentiment_chart = chart_service.generate_market_sentiment_chart(portfolio_data)
        
        return {
            "pie_chart": pie_chart,
            "performance_chart": performance_chart,
            "risk_chart": risk_chart,
            "sentiment_chart": sentiment_chart,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating charts: {str(e)}")

@app.get("/charts/stock/{symbol}")
async def get_stock_chart(symbol: str, period: str = "6mo"):
    """Get stock price chart"""
    try:
        chart_html = chart_service.generate_stock_price_chart(symbol, period)
        return {
            "symbol": symbol,
            "period": period,
            "chart": chart_html,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating stock chart: {str(e)}")

@app.get("/data/live-prices")
async def get_live_prices():
    """Get live stock prices"""
    try:
        portfolio_data = get_portfolio_data()
        symbols = [stock["symbol"] for stock in portfolio_data["stocks"]]
        live_prices = real_time_service.get_live_prices(symbols)
        
        return {
            "prices": live_prices,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching live prices: {str(e)}")

@app.get("/data/stock-info/{symbol}")
async def get_stock_info(symbol: str):
    """Get comprehensive stock information"""
    try:
        stock_info = real_time_service.get_stock_info(symbol)
        technical_indicators = real_time_service.calculate_technical_indicators(symbol)
        market_sentiment = real_time_service.get_market_sentiment(symbol)
        
        return {
            "symbol": symbol,
            "stock_info": stock_info,
            "technical_indicators": technical_indicators,
            "market_sentiment": market_sentiment,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock info: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

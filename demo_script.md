# Tech Conference Demo Script

## Financial Portfolio Analysis System Demo

### Introduction (2 minutes)
"Hello everyone! I'm Ganesh Divekar from Bajaj Technology, leading the India USA Mideast AI Team. Today, I'll demonstrate an AI-powered financial portfolio analysis system that showcases the power of multi-agent systems using LangGraph, FastAPI, and Mistral AI."

### System Overview (1 minute)
"This system features:
- 4 specialized AI agents working together
- Portfolio worth 80 lacs INR with Indian and US stocks
- Real-time news analysis and investment recommendations
- RAG system for personal information
- Support for both professional and Gen Z language styles"

---

## Demo Flow

### 1. System Startup (30 seconds)
```bash
# Start the server
python main.py
```
"Let me start the system. As you can see, it's running on localhost:8000 with all agents active."

### 2. Personal Introduction Query (1 minute)
**Query**: "Who is Ganesh Divekar?"
**Language**: Normal

**Expected Response**: Professional introduction with work details, experience, and contact information.

**Demo Point**: "Notice how the RAG agent retrieves my personal information from the vector database and provides a comprehensive response."

### 3. Portfolio Summary (1 minute)
**Query**: "Show me my portfolio summary"
**Language**: Gen Z

**Expected Response**: Emoji-rich response showing portfolio value, P&L, and performance status.

**Demo Point**: "The system adapts language style - here it's using Gen Z language with emojis and trendy expressions."

### 4. Penny Stocks Analysis (1 minute)
**Query**: "What are my penny stocks?"
**Language**: Normal

**Expected Response**: Detailed analysis of low-price stocks in the portfolio.

**Demo Point**: "The portfolio analyzer identifies penny stocks and provides performance metrics."

### 5. Investment Recommendations (1 minute)
**Query**: "What should I buy?"
**Language**: Gen Z

**Expected Response**: Buy recommendations with target prices and reasons.

**Demo Point**: "The investment advisor provides actionable recommendations based on market analysis."

### 6. News Impact Analysis (1 minute)
**Query**: "How does traffic issues in India affect my stocks?"
**Language**: Normal

**Expected Response**: Analysis of how traffic problems impact specific stocks in the portfolio.

**Demo Point**: "The news analyzer connects real-world events to portfolio impact."

### 7. Performance Analysis (1 minute)
**Query**: "Analyze my portfolio performance"
**Language**: Gen Z

**Expected Response**: Comprehensive performance analysis with emojis and insights.

**Demo Point**: "Multiple agents work together to provide comprehensive analysis."

### 8. Risk Assessment (1 minute)
**Query**: "Analyze my portfolio risk"
**Language**: Normal

**Expected Response**: Risk analysis with diversification score and recommendations.

**Demo Point**: "The system provides risk metrics and actionable advice."

---

## Technical Highlights

### Multi-Agent Architecture (1 minute)
"Let me show you the agent system architecture:"

```bash
# Check agent status
curl http://localhost:8000/agents/status
```

**Key Points**:
- 4 specialized agents working in coordination
- LangGraph orchestrates the workflow
- Each agent has specific expertise
- Agents can communicate and share data

### API Endpoints (30 seconds)
"Here are the main API endpoints:"
- `/chat` - Main conversation endpoint
- `/portfolio` - Portfolio analysis
- `/agents/status` - System status
- `/examples` - Query examples

### Vector Database (30 seconds)
"The RAG system uses ChromaDB for storing and retrieving personal information:"
- Embeddings for semantic search
- Context-aware responses
- Fallback mechanisms

---

## Advanced Features Demo

### 9. Sector Analysis (30 seconds)
**Query**: "Show sector breakdown"
**Language**: Normal

**Demo Point**: "Real-time sector analysis with value distribution."

### 10. Geographic Analysis (30 seconds)
**Query**: "Show country breakdown"
**Language**: Gen Z

**Demo Point**: "Geographic diversification analysis with emoji indicators."

### 11. Comprehensive Analysis (1 minute)
**Query**: "Give me a complete portfolio analysis with recommendations"
**Language**: Normal

**Demo Point**: "Multiple agents collaborate to provide comprehensive insights."

---

## Technical Deep Dive (2 minutes)

### LangGraph Workflow
"The system uses LangGraph to create a sophisticated workflow:"

1. **Query Classification**: Determines which agents to involve
2. **Agent Execution**: Runs relevant agents in sequence
3. **Response Combination**: Merges multiple agent outputs
4. **Final Response**: Delivers coherent, comprehensive answer

### Agent Communication
"Agents can communicate and share insights:"
- Portfolio data shared across agents
- News analysis informs investment advice
- Risk assessment considers multiple factors

### Error Handling
"The system includes robust error handling:"
- Graceful degradation if agents fail
- Fallback responses for API issues
- Comprehensive logging and monitoring

---

## Demo Scenarios for Audience

### Scenario 1: New Investor
**Query**: "I'm new to investing. What should I know about my portfolio?"
**Expected**: Educational response with basic concepts and portfolio overview.

### Scenario 2: Market Crisis
**Query**: "How should I react to market volatility?"
**Expected**: Risk management advice and portfolio protection strategies.

### Scenario 3: Technology Focus
**Query**: "Which tech stocks should I focus on?"
**Expected**: Technology sector analysis and specific recommendations.

---

## Q&A Preparation

### Common Questions:

1. **"How does the system handle real-time data?"**
   - Currently uses simulated data for demo
   - Can integrate with real APIs (yfinance, Alpha Vantage)
   - Supports real-time news feeds

2. **"What about data security?"**
   - Local vector database
   - No sensitive data stored
   - API key management
   - Session-based interactions

3. **"Can it handle multiple users?"**
   - Session management included
   - Scalable architecture
   - Concurrent request support

4. **"How accurate are the recommendations?"**
   - Educational purposes only
   - Not financial advice
   - Based on historical data and market trends

5. **"What's the cost of running this system?"**
   - Mistral AI free tier
   - Local ChromaDB (no cost)
   - Minimal infrastructure requirements

---

## Closing (1 minute)

"Thank you for your attention! This demo showcases:
- The power of multi-agent AI systems
- Real-world financial technology applications
- Scalable architecture with FastAPI
- Advanced AI capabilities with LangGraph and Mistral AI

The system demonstrates how AI can provide comprehensive financial analysis, making complex portfolio management accessible to everyone.

For questions or collaboration, you can reach me at 8459684546 or through Bajaj Technology.

Thank you!"

---

## Backup Demo Queries

If any demo fails, use these backup queries:

1. "What's my portfolio value?"
2. "Tell me about Ganesh's work experience"
3. "Give me investment advice"
4. "How does news affect investments?"
5. "Show me my best performing stocks"

## Technical Troubleshooting

### If API fails:
- Check API keys in config.py
- Verify internet connection
- Use fallback responses

### If agents fail:
- Check agent status endpoint
- Restart the application
- Use simplified responses

### If vector database fails:
- RAG agent will use fallback responses
- System continues to function
- Check ChromaDB installation

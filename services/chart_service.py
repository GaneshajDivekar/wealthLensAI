import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Any
from services.real_time_data import real_time_service

class ChartService:
    """Service for generating interactive charts and visualizations"""
    
    def __init__(self):
        self.colors = {
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#28a745',
            'danger': '#dc3545',
            'warning': '#ffc107',
            'info': '#17a2b8'
        }
    
    def generate_portfolio_pie_chart(self, portfolio_data: Dict[str, Any]) -> str:
        """Generate portfolio sector distribution pie chart"""
        try:
            # Prepare data for pie chart
            sector_data = {}
            for stock in portfolio_data['stocks']:
                sector = stock.get('sector', 'Unknown')
                current_value = stock.get('quantity', 0) * stock.get('current_price', 0)
                sector_data[sector] = sector_data.get(sector, 0) + current_value
            
            # Create pie chart
            fig = go.Figure(data=[go.Pie(
                labels=list(sector_data.keys()),
                values=list(sector_data.values()),
                hole=0.3,
                marker_colors=px.colors.qualitative.Set3
            )])
            
            fig.update_layout(
                title="Portfolio Sector Distribution",
                title_x=0.5,
                showlegend=True,
                height=400,
                margin=dict(t=50, b=50, l=50, r=50)
            )
            
            return fig.to_html(include_plotlyjs=False, full_html=False)
        except Exception as e:
            print(f"Error generating pie chart: {e}")
            return "<p>Chart generation failed</p>"
    
    def generate_portfolio_performance_chart(self, portfolio_data: Dict[str, Any]) -> str:
        """Generate portfolio performance bar chart"""
        try:
            # Prepare data for performance chart
            performance_data = []
            for stock in portfolio_data['stocks']:
                pnl_pct = stock.get('pnl_percentage', 0)
                performance_data.append({
                    'Stock': stock['name'],
                    'P&L %': pnl_pct,
                    'Sector': stock.get('sector', 'Unknown')
                })
            
            df = pd.DataFrame(performance_data)
            
            # Create bar chart
            fig = px.bar(
                df, 
                x='Stock', 
                y='P&L %',
                color='Sector',
                title="Portfolio Performance by Stock",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig.update_layout(
                title_x=0.5,
                height=400,
                margin=dict(t=50, b=50, l=50, r=50),
                xaxis_tickangle=-45
            )
            
            return fig.to_html(include_plotlyjs=False, full_html=False)
        except Exception as e:
            print(f"Error generating performance chart: {e}")
            return "<p>Chart generation failed</p>"
    
    def generate_stock_price_chart(self, symbol: str, period: str = "6mo") -> str:
        """Generate stock price chart with technical indicators"""
        try:
            # Get historical data
            hist = real_time_service.get_historical_data(symbol, period)
            if hist.empty:
                return "<p>No data available for chart</p>"
            
            # Create candlestick chart
            fig = go.Figure()
            
            # Add candlestick
            fig.add_trace(go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name='Price'
            ))
            
            # Add moving averages
            sma_20 = hist['Close'].rolling(window=20).mean()
            sma_50 = hist['Close'].rolling(window=50).mean()
            
            fig.add_trace(go.Scatter(
                x=hist.index,
                y=sma_20,
                mode='lines',
                name='SMA 20',
                line=dict(color='orange', width=1)
            ))
            
            fig.add_trace(go.Scatter(
                x=hist.index,
                y=sma_50,
                mode='lines',
                name='SMA 50',
                line=dict(color='red', width=1)
            ))
            
            fig.update_layout(
                title=f"{symbol} Price Chart",
                title_x=0.5,
                height=400,
                margin=dict(t=50, b=50, l=50, r=50),
                xaxis_title="Date",
                yaxis_title="Price"
            )
            
            return fig.to_html(include_plotlyjs=False, full_html=False)
        except Exception as e:
            print(f"Error generating stock chart: {e}")
            return "<p>Chart generation failed</p>"
    
    def generate_risk_metrics_chart(self, portfolio_data: Dict[str, Any]) -> str:
        """Generate risk metrics visualization"""
        try:
            # Calculate risk metrics
            total_value = sum(stock.get('quantity', 0) * stock.get('current_price', 0) for stock in portfolio_data['stocks'])
            
            # Sector concentration
            sector_concentration = {}
            for stock in portfolio_data['stocks']:
                sector = stock.get('sector', 'Unknown')
                value = stock.get('quantity', 0) * stock.get('current_price', 0)
                sector_concentration[sector] = sector_concentration.get(sector, 0) + value
            
            # Convert to percentages
            sector_percentages = {k: (v/total_value)*100 for k, v in sector_concentration.items()}
            
            # Create horizontal bar chart
            fig = go.Figure(data=[
                go.Bar(
                    x=list(sector_percentages.values()),
                    y=list(sector_percentages.keys()),
                    orientation='h',
                    marker_color=px.colors.qualitative.Set3
                )
            ])
            
            fig.update_layout(
                title="Sector Concentration Risk",
                title_x=0.5,
                height=400,
                margin=dict(t=50, b=50, l=50, r=50),
                xaxis_title="Percentage of Portfolio",
                yaxis_title="Sector"
            )
            
            return fig.to_html(include_plotlyjs=False, full_html=False)
        except Exception as e:
            print(f"Error generating risk chart: {e}")
            return "<p>Chart generation failed</p>"
    
    def generate_market_sentiment_chart(self, portfolio_data: Dict[str, Any]) -> str:
        """Generate market sentiment visualization"""
        try:
            # Get sentiment data for portfolio stocks
            sentiment_data = []
            for stock in portfolio_data['stocks']:
                symbol = stock['symbol']
                sentiment = real_time_service.get_market_sentiment(symbol)
                sentiment_data.append({
                    'Stock': stock['name'],
                    'Price Change %': sentiment.get('price_change_pct', 0),
                    'Sentiment': sentiment.get('sentiment', 'neutral')
                })
            
            df = pd.DataFrame(sentiment_data)
            
            # Create bar chart
            fig = px.bar(
                df,
                x='Stock',
                y='Price Change %',
                color='Sentiment',
                title="Market Sentiment by Stock",
                color_discrete_map={
                    'bullish': '#28a745',
                    'bearish': '#dc3545',
                    'neutral': '#6c757d'
                }
            )
            
            fig.update_layout(
                title_x=0.5,
                height=400,
                margin=dict(t=50, b=50, l=50, r=50),
                xaxis_tickangle=-45
            )
            
            return fig.to_html(include_plotlyjs=False, full_html=False)
        except Exception as e:
            print(f"Error generating sentiment chart: {e}")
            return "<p>Chart generation failed</p>"
    
    def generate_comprehensive_dashboard(self, portfolio_data: Dict[str, Any]) -> str:
        """Generate comprehensive dashboard with multiple charts"""
        try:
            # Generate all charts
            pie_chart = self.generate_portfolio_pie_chart(portfolio_data)
            performance_chart = self.generate_portfolio_performance_chart(portfolio_data)
            risk_chart = self.generate_risk_metrics_chart(portfolio_data)
            sentiment_chart = self.generate_market_sentiment_chart(portfolio_data)
            
            # Combine into dashboard
            dashboard_html = f"""
            <div class="dashboard-container">
                <div class="chart-row">
                    <div class="chart-item">
                        <h4>Portfolio Distribution</h4>
                        {pie_chart}
                    </div>
                    <div class="chart-item">
                        <h4>Performance Analysis</h4>
                        {performance_chart}
                    </div>
                </div>
                <div class="chart-row">
                    <div class="chart-item">
                        <h4>Risk Metrics</h4>
                        {risk_chart}
                    </div>
                    <div class="chart-item">
                        <h4>Market Sentiment</h4>
                        {sentiment_chart}
                    </div>
                </div>
            </div>
            """
            
            return dashboard_html
        except Exception as e:
            print(f"Error generating dashboard: {e}")
            return "<p>Dashboard generation failed</p>"

# Global instance
chart_service = ChartService()

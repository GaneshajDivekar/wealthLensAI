from typing import Dict, Any, List, Tuple
import re
from datetime import datetime

class ValidationService:
    """Service for validating data accuracy and response quality"""
    
    def __init__(self):
        self.confidence_thresholds = {
            "high": 0.8,
            "medium": 0.6,
            "low": 0.4
        }
    
    def validate_portfolio_data(self, portfolio_data: Dict) -> Dict[str, Any]:
        """Validate portfolio data for accuracy"""
        validation_result = {
            "is_valid": True,
            "confidence_score": 1.0,
            "issues": [],
            "warnings": []
        }
        
        try:
            # Check if portfolio data exists
            if not portfolio_data or 'stocks' not in portfolio_data:
                validation_result["is_valid"] = False
                validation_result["confidence_score"] = 0.0
                validation_result["issues"].append("Portfolio data is missing or invalid")
                return validation_result
            
            stocks = portfolio_data['stocks']
            
            # Validate each stock
            for i, stock in enumerate(stocks):
                stock_validation = self._validate_stock_data(stock, i)
                if not stock_validation["is_valid"]:
                    validation_result["issues"].extend(stock_validation["issues"])
                    validation_result["confidence_score"] *= 0.9
                
                if stock_validation["warnings"]:
                    validation_result["warnings"].extend(stock_validation["warnings"])
            
            # Check for data consistency
            total_value = sum(stock.get('quantity', 0) * stock.get('current_price', 0) for stock in stocks)
            if total_value <= 0:
                validation_result["issues"].append("Total portfolio value is zero or negative")
                validation_result["confidence_score"] *= 0.5
            
            # Check for reasonable price ranges
            for stock in stocks:
                price = stock.get('current_price', 0)
                if price > 100000:  # Unrealistic high price
                    validation_result["warnings"].append(f"Unusually high price for {stock.get('name', 'Unknown')}: ₹{price}")
                elif price < 0:
                    validation_result["issues"].append(f"Negative price for {stock.get('name', 'Unknown')}: ₹{price}")
                    validation_result["confidence_score"] *= 0.8
            
            return validation_result
            
        except Exception as e:
            validation_result["is_valid"] = False
            validation_result["confidence_score"] = 0.0
            validation_result["issues"].append(f"Validation error: {str(e)}")
            return validation_result
    
    def _validate_stock_data(self, stock: Dict, index: int) -> Dict[str, Any]:
        """Validate individual stock data"""
        validation = {
            "is_valid": True,
            "issues": [],
            "warnings": []
        }
        
        required_fields = ['symbol', 'name', 'quantity', 'current_price', 'avg_price']
        
        # Check required fields
        for field in required_fields:
            if field not in stock or stock[field] is None:
                validation["issues"].append(f"Missing required field '{field}' in stock {index}")
                validation["is_valid"] = False
        
        # Validate numeric fields
        if 'quantity' in stock and (not isinstance(stock['quantity'], (int, float)) or stock['quantity'] <= 0):
            validation["issues"].append(f"Invalid quantity for stock {index}: {stock['quantity']}")
            validation["is_valid"] = False
        
        if 'current_price' in stock and (not isinstance(stock['current_price'], (int, float)) or stock['current_price'] < 0):
            validation["issues"].append(f"Invalid current price for stock {index}: {stock['current_price']}")
            validation["is_valid"] = False
        
        if 'avg_price' in stock and (not isinstance(stock['avg_price'], (int, float)) or stock['avg_price'] < 0):
            validation["issues"].append(f"Invalid average price for stock {index}: {stock['avg_price']}")
            validation["is_valid"] = False
        
        return validation
    
    def validate_response_accuracy(self, query: str, response: str, expected_intent: str) -> Dict[str, Any]:
        """Validate response accuracy based on query intent"""
        validation = {
            "accuracy_score": 1.0,
            "relevance_score": 1.0,
            "confidence": "high",
            "issues": [],
            "suggestions": []
        }
        
        # Check if response is empty
        if not response or len(response.strip()) < 10:
            validation["accuracy_score"] = 0.0
            validation["relevance_score"] = 0.0
            validation["confidence"] = "low"
            validation["issues"].append("Response is too short or empty")
            return validation
        
        # Check for currency conversion requests
        if "usd" in query.lower() or "dollar" in query.lower():
            if "₹" in response and "$" not in response:
                validation["accuracy_score"] *= 0.7
                validation["issues"].append("Currency conversion requested but not provided")
                validation["suggestions"].append("Include USD conversion in response")
        
        # Check for specific price requests
        if "exact price" in query.lower() or "current price" in query.lower():
            if not re.search(r'₹\d+', response) and not re.search(r'\$\d+', response):
                validation["accuracy_score"] *= 0.8
                validation["issues"].append("Price requested but not found in response")
        
        # Check for personal info requests
        if "who am i" in query.lower() or "who is ganesh" in query.lower():
            if "ganesh" not in response.lower():
                validation["accuracy_score"] *= 0.6
                validation["issues"].append("Personal information requested but not provided")
        
        # Determine confidence level
        if validation["accuracy_score"] >= self.confidence_thresholds["high"]:
            validation["confidence"] = "high"
        elif validation["accuracy_score"] >= self.confidence_thresholds["medium"]:
            validation["confidence"] = "medium"
        else:
            validation["confidence"] = "low"
        
        return validation
    
    def add_confidence_disclaimer(self, response: str, confidence: str, issues: List[str]) -> str:
        """Add confidence disclaimer to response"""
        if confidence == "high":
            return response
        
        disclaimer = f"\n\n⚠️ **Confidence Level: {confidence.upper()}**"
        if issues:
            disclaimer += f"\n⚠️ **Issues Detected:** {', '.join(issues[:3])}"
        
        if confidence == "low":
            disclaimer += "\n💡 **Suggestion:** Please verify this information with official sources."
        
        return response + disclaimer

# Global instance
validation_service = ValidationService()

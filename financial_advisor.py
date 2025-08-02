import numpy as np
from typing import Dict, List
import random

class FinancialAdvisor:
    def __init__(self):
        self.risk_profile_questions = [
            "What is your investment time horizon?",
            "What is your risk tolerance?",
            "What are your financial goals?",
            "What is your current income level?",
            "Do you have any existing investments?"
        ]
        
    def analyze_risk_profile(self, answers: Dict) -> str:
        """
        Analyze user's risk profile based on their answers
        """
        risk_score = 0
        
        # Analyze answers
        if answers['time_horizon'] > 10:
            risk_score += 2
        if answers['risk_tolerance'] == 'high':
            risk_score += 3
        if answers['income_level'] > 100000:
            risk_score += 2
        
        # Determine risk profile
        if risk_score >= 6:
            return 'aggressive'
        elif risk_score >= 3:
            return 'moderate'
        else:
            return 'conservative'
    
    def generate_investment_advice(self, risk_profile: str, budget: float) -> Dict:
        """
        Generate personalized investment advice
        """
        advice = {
            'risk_profile': risk_profile,
            'recommended_allocation': {},
            'investment_strategies': []
        }
        
        if risk_profile == 'aggressive':
            advice['recommended_allocation'] = {
                'stocks': 0.7,
                'bonds': 0.2,
                'cash': 0.1
            }
            advice['investment_strategies'] = [
                "Consider index funds for market exposure",
                "Look into growth stocks in emerging sectors",
                "Keep emergency fund of 3-6 months expenses"
            ]
        
        elif risk_profile == 'moderate':
            advice['recommended_allocation'] = {
                'stocks': 0.5,
                'bonds': 0.3,
                'cash': 0.2
            }
            advice['investment_strategies'] = [
                "Consider balanced funds",
                "Focus on dividend-paying stocks",
                "Maintain diversified portfolio"
            ]
        
        else:  # conservative
            advice['recommended_allocation'] = {
                'stocks': 0.3,
                'bonds': 0.5,
                'cash': 0.2
            }
            advice['investment_strategies'] = [
                "Focus on fixed income",
                "Consider high-quality bonds",
                "Maintain liquidity"
            ]
        
        return advice
    
    def generate_savings_advice(self, expenses: Dict, income: float) -> Dict:
        """
        Generate savings advice based on spending patterns
        """
        # Calculate savings rate
        total_expenses = sum(expenses.values())
        savings_rate = (income - total_expenses) / income * 100
        
        # Generate advice
        advice = {
            'current_savings_rate': savings_rate,
            'recommended_savings_rate': 20,  # 20% rule
            'potential_improvements': []
        }
        
        # Analyze categories
        if expenses.get('entertainment', 0) > 0.1 * income:
            advice['potential_improvements'].append("Consider reducing entertainment expenses")
        if expenses.get('food', 0) > 0.15 * income:
            advice['potential_improvements'].append("Optimize grocery shopping")
        
        return advice

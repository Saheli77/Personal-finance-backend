import pandas as pd
from datetime import datetime
from typing import Dict, List

class BudgetAnalyzer:
    def __init__(self):
        self.categories = {
            'housing': ['rent', 'mortgage', 'utilities'],
            'food': ['groceries', 'dining out'],
            'transport': ['gas', 'public transport', 'car maintenance'],
            'entertainment': ['movies', 'hobbies', 'events'],
            'health': ['medical', 'gym', 'medication']
        }
        
    def categorize_expense(self, description: str) -> str:
        """
        Categorize an expense based on its description
        """
        description = description.lower()
        for category, keywords in self.categories.items():
            if any(keyword in description for keyword in keywords):
                return category
        return 'other'
    
    def analyze_spending(self, transactions: List[Dict]) -> Dict:
        """
        Analyze spending patterns and provide insights
        """
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['category'] = df['description'].apply(self.categorize_expense)
        
        # Monthly spending analysis
        monthly_spending = df.groupby(['category', pd.Grouper(key='date', freq='M')])['amount'].sum()
        
        # Category-wise analysis
        category_spending = df.groupby('category')['amount'].sum()
        
        # Insights
        insights = {
            'total_spending': df['amount'].sum(),
            'category_breakdown': category_spending.to_dict(),
            'monthly_trends': monthly_spending.to_dict(),
            'savings_potential': self.calculate_savings_potential(df)
        }
        
        return insights
    
    def calculate_savings_potential(self, df: pd.DataFrame) -> float:
        """
        Calculate potential savings based on spending patterns
        """
        # Calculate average spending in discretionary categories
        discretionary_categories = ['entertainment', 'food']
        discretionary_spending = df[df['category'].isin(discretionary_categories)]['amount'].sum()
        
        # Calculate potential savings (20% of discretionary spending)
        return discretionary_spending * 0.2

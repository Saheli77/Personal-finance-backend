import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

class FraudDetector:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        
    def train_model(self, transaction_data):
        """
        Train the fraud detection model using Isolation Forest
        """
        # Standardize the data
        scaled_data = self.scaler.fit_transform(transaction_data)
        
        # Train Isolation Forest
        self.model = IsolationForest(n_estimators=100, contamination='auto', random_state=42)
        self.model.fit(scaled_data)
        
        # Save the model and scaler
        joblib.dump(self.model, 'models/fraud_detection/model.pkl')
        joblib.dump(self.scaler, 'models/fraud_detection/scaler.pkl')
        
    def predict_fraud(self, transaction):
        """
        Predict if a transaction is fraudulent
        """
        if self.model is None:
            self.model = joblib.load('models/fraud_detection/model.pkl')
            self.scaler = joblib.load('models/fraud_detection/scaler.pkl')
        
        # Transform the transaction
        scaled_transaction = self.scaler.transform([transaction])
        
        # Predict
        prediction = self.model.predict(scaled_transaction)
        return prediction[0] == -1  # -1 indicates fraud, 1 indicates normal

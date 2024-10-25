import numpy as np
import pandas as pd

def risk_profile(age, income_stability, risk_tolerance):
    """
    Creates a risk profile score based on user-specific attributes.
    
    Parameters:
    - age (int): Age of the user.
    - income_stability (str): Stability of the user’s income ('stable', 'moderate', 'unstable').
    - risk_tolerance (str): User’s risk preference ('low', 'medium', 'high').

    Returns:
    - risk_score (float): Risk score used to adjust asset allocations.
    """
    # Base score adjustments for age, income stability, and risk tolerance
    age_factor = max(0, 100 - age) / 100  # Younger age suggests higher risk capacity
    stability_factor = {'stable': 1.0, 'moderate': 0.75, 'unstable': 0.5}.get(income_stability, 0.5)
    tolerance_factor = {'low': 0.5, 'medium': 0.75, 'high': 1.0}.get(risk_tolerance, 0.75)
    
    # Calculate combined risk score
    risk_score = age_factor * stability_factor * tolerance_factor
    return round(risk_score, 2)

def dynamic_allocation(risk_score, sentiment_data, financial_data):
    """
    Adjusts asset allocation based on user’s risk score and market sentiment.

    Parameters:
    - risk_score (float): Risk score derived from user-specific data.
    - sentiment_data (DataFrame): DataFrame with sentiment scores.
    - financial_data (DataFrame): DataFrame with historical asset returns and volatilities.

    Returns:
    - allocation (dict): Recommended percentage allocation for each asset class.
    """
    # Base allocations by risk tolerance level
    base_allocation = {'stocks': 0.4, 'bonds': 0.3, 'real_estate': 0.2, 'crypto': 0.1}

    # Modify allocations based on risk score and sentiment analysis
    for asset in base_allocation:
        # Adjust stock allocation if sentiment is positive
        if asset == 'stocks' and sentiment_data[sentiment_data['ticker'] == 'NSEI']['sentiment_score'].mean() > 0:
            base_allocation[asset] += risk_score * 0.1
        # Reduce bond allocation in high-risk scores
        elif asset == 'bonds':
            base_allocation[asset] -= (1 - risk_score) * 0.1
        # Increase or decrease crypto and real estate based on score
        elif asset == 'crypto' and risk_score > 0.7:
            base_allocation[asset] += 0.05
        elif asset == 'real_estate' and risk_score < 0.5:
            base_allocation[asset] -= 0.05

    # Normalize allocations to ensure they add up to 100%
    total_allocation = sum(base_allocation.values())
    allocation = {asset: round((percentage / total_allocation) * 100, 2) for asset, percentage in base_allocation.items()}

    return allocation

# Example usage
user_data = {
    "age": 30,
    "income_stability": "stable",
    "risk_tolerance": "high"
}

# Mocked financial and sentiment data
sentiment_data = pd.DataFrame({
    "ticker": ["NSEI", "BND", "VNQ", "BTC-USD"],
    "sentiment_score": [0.1, 0.02, -0.03, 0.05]
})
financial_data = pd.DataFrame({
    "ticker": ["NSEI", "BND", "VNQ", "BTC-USD"],
    "annualized_return": [0.12, 0.04, 0.07, 0.15],
    "annualized_volatility": [0.18, 0.05, 0.12, 0.25]
})

risk_score = risk_profile(user_data["age"], user_data["income_stability"], user_data["risk_tolerance"])
allocation = dynamic_allocation(risk_score, sentiment_data, financial_data)

print("Risk Score:", risk_score)
print("Recommended Allocation:", allocation)


# Explanation
# Risk Profile Score:

# Combines age, income stability, and risk tolerance into a single score (0 to 1).
# A higher score suggests a higher risk appetite.
# Dynamic Allocation:

# Base allocations (e.g., 40% stocks) adjust based on the risk score.
# Sentiment data helps modify stock allocation in response to positive/negative market sentiment.
# Bond, crypto, and real estate allocations vary based on risk profile, ensuring user preferences and market conditions are respected.
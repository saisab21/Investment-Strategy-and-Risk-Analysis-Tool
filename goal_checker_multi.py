import numpy as np
import pandas as pd
from tax_adjustment import apply_taxes_and_fees, adjust_for_inflation


def monte_carlo_simulation_multi(initial_investment, annual_return, annual_volatility, years, num_simulations=1000):
    projections = []
    for _ in range(num_simulations):
        yearly_growth = np.random.normal(annual_return, annual_volatility, years)
        end_value = initial_investment
        for growth in yearly_growth:
            end_value *= (1 + growth)
        projections.append(end_value)
    return projections

def check_multi_goal_feasibility(initial_investment, goals, asset_allocation, financial_data, tax_rates, fees, inflation_rate):
    results = {}
    total_investment = initial_investment
    for goal_name, goal in goals.items():
        # Goal-specific details
        goal_amount = goal["goal_amount"]
        timeline_years = goal["timeline_years"]
        priority = goal["priority"]

        # Adjust allocation based on goal priority
        allocation = asset_allocation.copy()
        if priority == "high":
            allocation["bonds"] += 0.1
            allocation["crypto"] -= 0.1
        elif priority == "low":
            allocation["stocks"] += 0.1
            allocation["bonds"] -= 0.1

        # Calculate weighted return and volatility
        weighted_return = 0
        weighted_volatility = 0
        for asset, allocation_percent in allocation.items():
            asset_return = financial_data[financial_data['ticker'] == asset]['annualized_return'].values[0]
            asset_volatility = financial_data[financial_data['ticker'] == asset]['annualized_volatility'].values[0]
            weight = allocation_percent / 100
            weighted_return += weight * asset_return
            weighted_volatility += weight * asset_volatility

        # Run simulation
        projections = monte_carlo_simulation_multi(total_investment, weighted_return, weighted_volatility, timeline_years)
        adjusted_projections = apply_taxes_and_fees(projections, tax_rates, fees, timeline_years)
        inflation_adjusted_projections = adjust_for_inflation(adjusted_projections, inflation_rate, timeline_years)

        # Goal success probability and recommendation
        success_probability = len([p for p in inflation_adjusted_projections if p >= goal_amount]) / len(inflation_adjusted_projections) * 100
        recommendation = "Goal is achievable" if success_probability >= 75 else "Increase investment or extend timeline."

        results[goal_name] = {
            "goal_amount": goal_amount,
            "timeline_years": timeline_years,
            "priority": priority,
            "success_probability": round(success_probability, 2),
            "median_projection": round(np.median(inflation_adjusted_projections), 2),
            "projection_range": (round(np.percentile(inflation_adjusted_projections, 25), 2), 
                                 round(np.percentile(inflation_adjusted_projections, 75), 2)),
            "recommendation": recommendation
        }
    
    return results

# Example usage with multiple goals
goals = {
    "House": {"goal_amount": 2000000, "timeline_years": 15, "priority": "high"},
    "Retirement": {"goal_amount": 10000000, "timeline_years": 30, "priority": "medium"},
    "Education": {"goal_amount": 1000000, "timeline_years": 10, "priority": "low"}
}
initial_investment = 1000000
asset_allocation = {"stocks": 50, "bonds": 30, "real_estate": 10, "crypto": 10}
financial_data = pd.DataFrame({
    "ticker": ["stocks", "bonds", "real_estate", "crypto"],
    "annualized_return": [0.12, 0.04, 0.07, 0.15],
    "annualized_volatility": [0.18, 0.05, 0.12, 0.25]
})
tax_rates = {"short_term": 0.15, "long_term": 0.10}
fees = {"stocks": 0.5, "bonds": 0.2, "real_estate": 0.3, "crypto": 0.8}
inflation_rate = 0.05

multi_goal_results = check_multi_goal_feasibility(initial_investment, goals, asset_allocation, financial_data, tax_rates, fees, inflation_rate)
print(multi_goal_results)

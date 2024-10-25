import numpy as np
import pandas as pd

def monte_carlo_simulation(initial_investment, annual_return, annual_volatility, years, num_simulations=1000):
    """
    Runs a Monte Carlo simulation to project future investment values.
    
    Parameters:
    - initial_investment (float): Starting capital.
    - annual_return (float): Expected annual return rate.
    - annual_volatility (float): Annual volatility of returns.
    - years (int): Investment horizon in years.
    - num_simulations (int): Number of simulation runs.
    
    Returns:
    - projections (list): List of simulated end values for each run.
    """
    projections = []
    for _ in range(num_simulations):
        yearly_growth = np.random.normal(annual_return, annual_volatility, years)
        end_value = initial_investment
        for growth in yearly_growth:
            end_value *= (1 + growth)
        projections.append(end_value)
    return projections

def check_goal_feasibility(initial_investment, goal_amount, timeline_years, asset_allocation, financial_data):
    """
    Evaluates if the user’s financial goal is feasible and provides suggestions if adjustments are needed.
    
    Parameters:
    - initial_investment (float): Capital the user is willing to invest.
    - goal_amount (float): Target future amount.
    - timeline_years (int): Investment horizon in years.
    - asset_allocation (dict): Percentage allocations for each asset class.
    - financial_data (DataFrame): DataFrame containing returns and volatilities for assets.
    
    Returns:
    - result (dict): Feasibility status, projected values, and recommendations.
    """
    # Weighted average return and volatility based on allocation and financial data
    weighted_return = 0
    weighted_volatility = 0
    for asset, allocation_percent in asset_allocation.items():
        asset_return = financial_data[financial_data['ticker'] == asset]['annualized_return'].values[0]
        asset_volatility = financial_data[financial_data['ticker'] == asset]['annualized_volatility'].values[0]
        weight = allocation_percent / 100
        weighted_return += weight * asset_return
        weighted_volatility += weight * asset_volatility

    # Run Monte Carlo simulations to project future value
    projections = monte_carlo_simulation(initial_investment, weighted_return, weighted_volatility, timeline_years)
    
    # Calculate probability of achieving the goal
    successful_runs = [p for p in projections if p >= goal_amount]
    probability_of_success = len(successful_runs) / len(projections) * 100

    # Recommendations based on success probability
    recommendation = "Goal is achievable with current inputs." if probability_of_success >= 75 else (
        "Consider increasing investment, extending timeline, or adjusting risk tolerance."
    )

    # Compile result
    result = {
        "initial_investment": initial_investment,
        "goal_amount": goal_amount,
        "timeline_years": timeline_years,
        "probability_of_success": round(probability_of_success, 2),
        "recommendation": recommendation,
        "median_projection": round(np.median(projections), 2),
        "projection_range": (round(np.percentile(projections, 25), 2), round(np.percentile(projections, 75), 2))
    }

    return result

# Example usage
user_goal = {
    "initial_investment": 50000,
    "goal_amount": 150000,
    "timeline_years": 10
}
asset_allocation = {"stocks": 50, "bonds": 30, "real_estate": 10, "crypto": 10}
financial_data = pd.DataFrame({
    "ticker": ["stocks", "bonds", "real_estate", "crypto"],
    "annualized_return": [0.12, 0.04, 0.07, 0.15],
    "annualized_volatility": [0.18, 0.05, 0.12, 0.25]
})

feasibility_result = check_goal_feasibility(
    user_goal["initial_investment"],
    user_goal["goal_amount"],
    user_goal["timeline_years"],
    asset_allocation,
    financial_data
)
print(feasibility_result)


# Explanation of Key Components
# Monte Carlo Simulation:

# Uses the user’s asset allocation and financial data to simulate different return scenarios over the investment period.
# Returns an array of possible end values, providing a range of expected outcomes.
# Goal Feasibility:

# Calculates the probability of reaching the user’s goal by determining the proportion of simulations that achieve or exceed the target amount.
# If the probability is below 75%, it suggests increasing capital, timeline, or risk tolerance to improve goal attainment chances.
# Result Output:

# Provides median projection, a 25th-75th percentile range, and an actionable recommendation based on feasibility.
# This module allows for a realistic assessment of goal attainability, providing a probabilistic view of future outcomes. 
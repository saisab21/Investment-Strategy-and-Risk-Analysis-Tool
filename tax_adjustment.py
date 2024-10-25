import numpy as np

def apply_taxes_and_fees(projections, tax_rates, fees, holding_period):
    """
    Applies capital gains tax and transaction fees to each projection.
    
    Parameters:
    - projections (list): List of projected end values.
    - tax_rates (dict): Tax rates for 'short_term' and 'long_term' gains.
    - fees (dict): Transaction fees as percentages for each asset class.
    - holding_period (int): Number of years the investment is held.
    
    Returns:
    - adjusted_projections (list): Projections adjusted for tax and fees.
    """
    adjusted_projections = []
    tax_rate = tax_rates['long_term'] if holding_period >= 1 else tax_rates['short_term']
    
    for value in projections:
        # Apply fees
        after_fees = value * (1 - sum(fees.values()) / 100)
        # Apply tax on gains
        taxable_gain = max(0, after_fees - value)
        after_tax = after_fees - (taxable_gain * tax_rate)
        adjusted_projections.append(after_tax)
    
    return adjusted_projections

def adjust_for_inflation(projections, inflation_rate, years):
    """
    Adjusts projections for inflation to reflect real purchasing power.
    
    Parameters:
    - projections (list): List of projected end values after tax and fees.
    - inflation_rate (float): Annual inflation rate (e.g., 0.05 for 5%).
    - years (int): Investment horizon in years.
    
    Returns:
    - inflation_adjusted_projections (list): Projections adjusted for inflation.
    """
    inflation_adjusted_projections = [p / ((1 + inflation_rate) ** years) for p in projections]
    return inflation_adjusted_projections

def calculate_net_projections(initial_investment, goal_amount, projections, tax_rates, fees, inflation_rate, holding_period):
    """
    Calculates net projections by applying taxes, fees, and inflation adjustment.
    
    Parameters:
    - initial_investment (float): Capital invested.
    - goal_amount (float): Target amount the user wants to reach.
    - projections (list): List of Monte Carlo simulation projections.
    - tax_rates (dict): Tax rates for short-term and long-term gains.
    - fees (dict): Transaction fees for each asset class.
    - inflation_rate (float): Expected annual inflation rate.
    - holding_period (int): Investment period in years.
    
    Returns:
    - result (dict): Net projections, probability of success, and goal feasibility status.
    """
    # Adjust for taxes and fees
    adjusted_projections = apply_taxes_and_fees(projections, tax_rates, fees, holding_period)
    # Adjust for inflation
    inflation_adjusted_projections = adjust_for_inflation(adjusted_projections, inflation_rate, holding_period)

    # Probability of meeting the goal
    success_probability = len([p for p in inflation_adjusted_projections if p >= goal_amount]) / len(inflation_adjusted_projections) * 100
    recommendation = "Goal is feasible after adjustments." if success_probability >= 75 else "Increase investment, adjust timeline, or reduce fees."

    return {
        "initial_investment": initial_investment,
        "goal_amount": goal_amount,
        "probability_of_success": round(success_probability, 2),
        "recommendation": recommendation,
        "median_projection": round(np.median(inflation_adjusted_projections), 2),
        "projection_range": (round(np.percentile(inflation_adjusted_projections, 25), 2), 
                             round(np.percentile(inflation_adjusted_projections, 75), 2))
    }

# Example usage
initial_investment = 50000
goal_amount = 150000
holding_period = 10
projections = [100000, 120000, 130000, 140000, 150000, 160000]  # Sample projections from Monte Carlo
tax_rates = {"short_term": 0.15, "long_term": 0.10}  # Placeholder rates for Indian market
fees = {"stocks": 0.5, "bonds": 0.2, "real_estate": 0.3, "crypto": 0.8}  # Fees in percent
inflation_rate = 0.05  # 5% annual inflation

result = calculate_net_projections(initial_investment, goal_amount, projections, tax_rates, fees, inflation_rate, holding_period)
print(result)


# Explanation of Key Components
# Taxes and Fees:
# Applies tax rates based on holding period (e.g., short-term vs. long-term capital gains) and transaction fees per asset.
# Inflation Adjustment:
# Adjusts future projections for inflation to provide real purchasing power, making the tool more realistic for long-term planning.
# Goal Feasibility:
# Provides a success probability and recommendation after accounting for taxes, fees, and inflation, helping users make informed decisions.
# This module ensures realistic, after-tax projections, making goal recommendations more precise.